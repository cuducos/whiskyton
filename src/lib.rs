use chrono::{DateTime, Utc};
use std::{fs, time::SystemTime};
use walkdir::WalkDir;

use pyo3::{pyfunction, pymodule, types::PyModule, wrap_pyfunction, PyResult, Python};

#[pyfunction]
fn pearson_r(x: Vec<u32>, y: Vec<u32>) -> PyResult<f64> {
    let n = x.len() as f64;
    let sum_x = x.iter().sum::<u32>() as f64;
    let sum_y = y.iter().sum::<u32>() as f64;
    let sum_x_sq = x.iter().map(|&i| i.pow(2)).sum::<u32>();
    let sum_y_sq = y.iter().map(|&i| i.pow(2)).sum::<u32>();
    let p_sum = x.iter().zip(y).map(|(i, j)| i * j).sum::<u32>();
    let num = (p_sum as f64) - ((sum_x * sum_y) / n);
    let multiplier_x: f64 = (sum_x_sq as f64) - ((sum_x.powi(2)) / n);
    let multiplier_y: f64 = (sum_y_sq as f64) - ((sum_y.powi(2)) / n);
    let den = (multiplier_x * multiplier_y).sqrt();
    if den != 0.0 {
        Ok(num / den)
    } else {
        Ok(0.0)
    }
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

#[pymodule]
fn crates(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(latest_changed_at, m)?)?;
    m.add_function(wrap_pyfunction!(pearson_r, m)?)?;
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
    fn test_pearson_r() {
        let expected = 0.7904333328627509;
        let x = vec![2, 2, 3, 1, 0, 2, 2, 1, 1, 1, 1, 2];
        let y = vec![2, 2, 3, 1, 0, 2, 1, 1, 1, 2, 1, 1];
        assert_eq!(pearson_r(x, y).unwrap(), expected);
    }
}
