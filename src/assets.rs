use anyhow::Result;
use lazy_static::lazy_static;
use serde::Serialize;

use crate::whisky::WHISKIES;

lazy_static! {
    pub static ref CSS: &'static [u8] = include_bytes!("static/style.css");
    pub static ref JS: &'static [u8] = include_bytes!("static/app.js");
    pub static ref BOTS: &'static [u8] = include_bytes!("static/robots.txt");
    pub static ref FAVICON: &'static [u8] = include_bytes!("static/favicon.ico");
}

pub fn by_name(name: &str) -> Option<&[u8]> {
    match name {
        "style.css" => Some(CSS.as_ref()),
        "app.js" => Some(JS.as_ref()),
        "robots.txt" => Some(BOTS.as_ref()),
        "favicon.ico" => Some(FAVICON.as_ref()),
        _ => None,
    }
}

#[derive(Serialize)]
pub struct AutocompleteData<'a> {
    pub whiskies: Vec<&'a str>,
}

impl<'a> AutocompleteData<'a> {
    pub fn new() -> Self {
        Self {
            whiskies: WHISKIES.iter().map(|w| w.distillery.as_str()).collect(),
        }
    }
    pub fn as_json(&self) -> Result<String> {
        Ok(serde_json::to_string(self)?)
    }
}
