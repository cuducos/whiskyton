use std::cmp::Ordering;

use anyhow::{anyhow, Result};
use csv::{ReaderBuilder, StringRecord};
use lazy_static::lazy_static;
use rayon::iter::{IntoParallelRefIterator, ParallelIterator};
use regex::Regex;

use crate::correlation::Correlation;

const DATA: &str = include_str!("data/whisky.csv");

lazy_static! {
    pub static ref WHISKIES: Vec<Whisky> = {
        let mut reader = ReaderBuilder::new()
            .has_headers(true)
            .from_reader(DATA.as_bytes());

        let mut whiskies: Vec<Whisky> = vec![];
        for row in reader.records() {
            let record = Whisky::from_csv_row(&row.unwrap()).unwrap();
            whiskies.push(record);
        }
        whiskies
    };
}

fn distillery(row: &StringRecord) -> Result<String> {
    row.get(0)
        .map(|v| v.to_string())
        .ok_or(anyhow!("Missing distillery name"))
}

fn taste(row: &StringRecord, idx: usize) -> Result<u32> {
    let val = row.get(idx).ok_or(anyhow!("Missing taste #{}", idx))?;
    Ok(val.parse::<u32>()?)
}

pub type PyWhisky = (String, String, [u32; 12]);

pub struct Whisky {
    pub distillery: String,
    pub body: u32,
    pub sweetness: u32,
    pub smoky: u32,
    pub medicinal: u32,
    pub tobacco: u32,
    pub honey: u32,
    pub spicy: u32,
    pub winey: u32,
    pub nutty: u32,
    pub malty: u32,
    pub fruity: u32,
    pub floral: u32,
}

impl Whisky {
    fn from_csv_row(row: &StringRecord) -> Result<Self> {
        Ok(Self {
            distillery: distillery(row)?,
            body: taste(row, 1)?,
            sweetness: taste(row, 2)?,
            smoky: taste(row, 3)?,
            medicinal: taste(row, 4)?,
            tobacco: taste(row, 5)?,
            honey: taste(row, 6)?,
            spicy: taste(row, 7)?,
            winey: taste(row, 8)?,
            nutty: taste(row, 9)?,
            malty: taste(row, 10)?,
            fruity: taste(row, 11)?,
            floral: taste(row, 12)?,
        })
    }

    fn slug(&self) -> String {
        Regex::new(r"[^a-z]+")
            .unwrap()
            .replace_all(self.distillery.to_lowercase().as_str(), "")
            .to_string()
    }

    pub fn tastes(&self) -> [u32; 12] {
        [
            self.body,
            self.sweetness,
            self.smoky,
            self.medicinal,
            self.tobacco,
            self.honey,
            self.spicy,
            self.winey,
            self.nutty,
            self.malty,
            self.fruity,
            self.floral,
        ]
    }

    pub fn py(&self) -> PyWhisky {
        (self.distillery.clone(), self.slug(), self.tastes())
    }
}

pub fn recommendations_for(name: String) -> Result<Vec<(PyWhisky, PyWhisky, f64)>> {
    let mut whisky: Option<&Whisky> = None;
    let mut others: Vec<&Whisky> = vec![];
    for w in WHISKIES.iter() {
        if w.distillery == name || w.slug() == name {
            whisky = Some(w);
        } else {
            others.push(w);
        }
    }
    let reference = whisky.ok_or(anyhow!("Whisky {} not found", name))?;
    let mut correlations: Vec<Correlation> = others
        .par_iter()
        .map(|w| Correlation::new(reference, w))
        .collect();

    correlations.sort_by(|a, b| {
        if a.value > b.value {
            Ordering::Less
        } else if a.value < b.value {
            Ordering::Greater
        } else {
            Ordering::Equal
        }
    });

    let best = correlations
        .iter()
        .take(9)
        .map(|c| (c.whisky.py(), c.other.py(), c.value))
        .collect::<Vec<(PyWhisky, PyWhisky, f64)>>();

    Ok(best)
}

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn test_all_whiskies_are_loaded() {
        assert_eq!(WHISKIES.len(), 86);
    }
}
