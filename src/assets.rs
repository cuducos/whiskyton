use std::collections::HashMap;

use anyhow::Result;
use lazy_static::lazy_static;
use serde::Serialize;

use crate::whisky::WHISKIES;

lazy_static! {
    pub static ref ASSETS: HashMap<String, Vec<u8>> = {
        let mut m = HashMap::new();
        m.insert(
            "style.css".to_string(),
            include_str!("static/style.css").to_string().into_bytes(),
        );
        m.insert(
            "app.js".to_string(),
            include_str!("static/app.js").to_string().into_bytes(),
        );
        m.insert(
            "robots.txt".to_string(),
            include_str!("static/robots.txt").to_string().into_bytes(),
        );
        m.insert(
            "favicon.ico".to_string(),
            include_bytes!("static/favicon.ico").to_vec(),
        );
        m
    };
}

#[derive(Serialize)]
pub struct AutocompleteData {
    pub whiskies: Vec<String>,
}

impl AutocompleteData {
    pub fn new() -> Self {
        Self {
            whiskies: WHISKIES.iter().map(|w| w.distillery.clone()).collect(),
        }
    }
    pub fn as_json(&self) -> Result<String> {
        Ok(serde_json::to_string(self)?)
    }
}
