use std::{fs, time::SystemTime};

use anyhow::Result;
use chrono::{DateTime, Utc};
use lazy_static::lazy_static;
use tera::{Context, Tera};
use walkdir::WalkDir;

use crate::whisky::WHISKIES;

lazy_static! {
    static ref TEMPLATE: Tera = {
        let mut tera = Tera::default();
        tera.add_raw_template("sitemap", include_str!("templates/sitemap.xml"))
            .unwrap();
        tera
    };
}

fn latest_changed_at(dir: String) -> Result<String> {
    let mut latest = SystemTime::UNIX_EPOCH;
    for pth in WalkDir::new(dir).into_iter().filter_map(|p| p.ok()) {
        if !pth.file_type().is_file() {
            continue;
        }
        let modified = fs::metadata(pth.path())?.modified()?;
        if modified > latest {
            latest = modified;
        }
    }
    let as_date: DateTime<Utc> = latest.into();
    Ok(as_date.format("%Y-%m-%d").to_string())
}

pub fn sitemap(root_url: String, root_dir: String) -> Result<String> {
    let whiskies = WHISKIES
        .iter()
        .map(|w| w.slug.as_str())
        .collect::<Vec<&str>>();

    let mut ctx = Context::new();
    ctx.insert("root", root_url.as_str());
    ctx.insert("last_change", latest_changed_at(root_dir)?.as_str());
    ctx.insert("whiskies", &whiskies);

    Ok(TEMPLATE.render("sitemap", &ctx)?)
}

#[cfg(test)]
mod tests {

    use std::fs;

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
    fn test_sitemap() {
        let got = sitemap(
            "http://whiskyton.onrender.com/".to_string(),
            tempfile::tempdir()
                .unwrap()
                .path()
                .to_string_lossy()
                .to_string(),
        )
        .unwrap();
        for whisky in WHISKIES.iter() {
            let expected = format!("http://whiskyton.onrender.com/{}/", whisky.slug);
            assert!(
                got.as_str().contains(expected.as_str()),
                "{expected} not found in {got}"
            );
        }
    }
}
