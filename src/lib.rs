use std::{fs, time::SystemTime};

use chrono::{DateTime, Utc};
use mime_guess::from_path;
use pyo3::{
    exceptions::PyValueError,
    pyfunction, pymodule,
    types::{PyBytes, PyModule},
    wrap_pyfunction, PyObject, PyResult, Python, ToPyObject,
};
use rand::Rng;
use walkdir::WalkDir;

mod assets;
mod correlation;
mod whisky;

#[pyfunction]
fn pearson_r(x: [u32; 12], y: [u32; 12]) -> PyResult<f64> {
    Ok(correlation::pearson_r(x, y))
}

#[pyfunction]
fn latest_changed_at(dir: String) -> PyResult<String> {
    let mut latest = SystemTime::UNIX_EPOCH;
    for pth in WalkDir::new(dir).into_iter().filter_map(|p| p.ok()) {
        if !pth.file_type().is_file() {
            continue;
        }
        if let Ok(meta) = fs::metadata(pth.path()) {
            if let Ok(modified) = meta.modified() {
                if modified > latest {
                    latest = modified;
                }
            }
        }
    }
    let as_date: DateTime<Utc> = latest.into();
    Ok(as_date.format("%Y-%m-%d").to_string())
}

#[pyfunction]
fn recommendations_for(name: String) -> PyResult<Vec<(whisky::PyWhisky, whisky::PyWhisky, f64)>> {
    whisky::recommendations_for(name).map_err(|e| PyValueError::new_err(e.to_string()))
}

#[pyfunction]
fn all_whiskies() -> PyResult<Vec<whisky::PyWhisky>> {
    Ok(whisky::WHISKIES.iter().map(|w| w.py()).collect())
}

#[pyfunction]
fn random_whisky() -> PyResult<whisky::PyWhisky> {
    let mut rng = rand::thread_rng();
    let idx = rng.gen_range(0..whisky::WHISKIES.len());
    Ok(whisky::WHISKIES[idx].py())
}

#[pyfunction]
fn asset(py: Python, name: &str) -> PyResult<(PyObject, String)> {
    let mut bytes: &[u8] = &[];
    if name == "whiskyton.json" {
        bytes = &whisky::AUTOCOMPLETE;
    }
    if let Some(b) = assets::ASSETS.get(name) {
        bytes = b
    }
    if bytes.is_empty() {
        return PyResult::Err(PyValueError::new_err(format!("Asset {name} not found")));
    }
    let mime = from_path(name).first().map(|m| m.to_string()).ok_or(PyValueError::new_err(format!("No mimetype found for {name}")))?;
    Ok((
        PyBytes::new(py, bytes).to_object(py), mime))
}

#[pymodule]
fn crates(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(latest_changed_at, m)?)?;
    m.add_function(wrap_pyfunction!(pearson_r, m)?)?;
    m.add_function(wrap_pyfunction!(recommendations_for, m)?)?;
    m.add_function(wrap_pyfunction!(random_whisky, m)?)?;
    m.add_function(wrap_pyfunction!(all_whiskies, m)?)?;
    m.add_function(wrap_pyfunction!(asset, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn test_latest_changed_at() {
        let tmp = tempfile::tempdir().unwrap();
        let pth = tmp.path().join("answer.txt");
        fs::write(pth, "42").unwrap();
        let today = SystemTime::now();
        let expected: DateTime<Utc> = today.into();
        let got = latest_changed_at(tmp.path().to_string_lossy().to_string());
        assert_eq!(got.unwrap(), expected.format("%Y-%m-%d").to_string());
    }

    #[test]
    fn test_asset_mimetype() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| -> PyResult<()> {
            let test_cases: Vec<(&str, &str)> = vec![
                ("style.css", "text/css"),
                ("app.js", "application/javascript"),
                ("whiskyton.json", "application/json"),
                ("robots.txt", "text/plain"),
                ("favicon.ico", "image/x-icon"),
            ];
            for (name, expected) in test_cases.iter() {
                let (_, got) = asset(py, name).unwrap();
                assert_eq!(got, expected.to_string());
            }
            Ok(())
        })
        .unwrap();
    }
}
