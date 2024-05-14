use mime_guess::from_path;
use pyo3::{
    exceptions::PyValueError,
    pyfunction, pymodule,
    types::{PyBytes, PyModule},
    wrap_pyfunction, PyObject, PyResult, Python, ToPyObject,
};
use rand::Rng;

mod assets;
mod chart;
mod correlation;
mod sitemap;
mod whisky;

#[pyfunction]
fn recommendations_for(name: String) -> PyResult<whisky::PyWhisky> {
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
    let mime = from_path(name)
        .first()
        .map(|m| m.to_string())
        .ok_or(PyValueError::new_err(format!(
            "No mimetype found for {name}"
        )))?;
    Ok((PyBytes::new(py, bytes).to_object(py), mime))
}

#[pyfunction]
fn render_sitemap(py: Python, root_url: String, root_dir: String) -> PyResult<PyObject> {
    let contents =
        sitemap::sitemap(root_url, root_dir).map_err(|e| PyValueError::new_err(e.to_string()))?;
    Ok(PyBytes::new(py, &contents.into_bytes()).to_object(py))
}

#[pymodule]
fn crates(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(recommendations_for, m)?)?;
    m.add_function(wrap_pyfunction!(random_whisky, m)?)?;
    m.add_function(wrap_pyfunction!(all_whiskies, m)?)?;
    m.add_function(wrap_pyfunction!(asset, m)?)?;
    m.add_function(wrap_pyfunction!(render_sitemap, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {

    use super::*;

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
