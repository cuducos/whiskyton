use chrono::{DateTime, Utc};
use std::{fs, time::SystemTime};
use walkdir::WalkDir;

use pyo3::{pyfunction, pymodule, types::PyModule, wrap_pyfunction, PyResult, Python};

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

#[pymodule]
fn crates(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(latest_changed_at, m)?)?;
    Ok(())
}
