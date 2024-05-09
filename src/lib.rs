use std::{fs, time::SystemTime};

use chrono::{DateTime, Utc};
use pyo3::{
    exceptions::PyValueError, pyfunction, pymodule, types::PyModule, wrap_pyfunction, PyResult,
    Python,
};
use walkdir::WalkDir;

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
fn random_whisky() -> PyResult<whisky::PyWhisky> {
    whisky::random_whisky().map_err(|e| PyValueError::new_err(e.to_string()))
}

#[pyfunction]
fn all_whiskies() -> PyResult<Vec<whisky::PyWhisky>> {
    whisky::all_whiskies().map_err(|e| PyValueError::new_err(e.to_string()))
}

#[pymodule]
fn crates(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(latest_changed_at, m)?)?;
    m.add_function(wrap_pyfunction!(pearson_r, m)?)?;
    m.add_function(wrap_pyfunction!(recommendations_for, m)?)?;
    m.add_function(wrap_pyfunction!(random_whisky, m)?)?;
    m.add_function(wrap_pyfunction!(all_whiskies, m)?)?;
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
}
