use std::cmp::Ordering;

use anyhow::{anyhow, Result};
use csv::{ReaderBuilder, StringRecord};
use lazy_static::lazy_static;
use rayon::iter::{IntoParallelRefIterator, IntoParallelRefMutIterator, ParallelIterator};
use rayon::slice::ParallelSliceMut;
use regex::Regex;

use crate::assets::AutocompleteData;
use crate::correlation::{Correlation, PyCorrelation};

const DATA: &str = include_str!("static/whisky.csv");

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
    pub static ref AUTOCOMPLETE: Vec<u8> = AutocompleteData::new().as_json().unwrap().into_bytes();
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

pub type PyWhisky = (
    String,                                     // distillery
    String,                                     // slug
    [u32; 12],                                  // tastes
    Option<Vec<(f64, String, Option<String>)>>, // correlations
);

#[derive(Clone)]
pub struct Tastes {
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

impl Tastes {
    pub fn as_array(&self) -> [u32; 12] {
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
}

#[derive(Clone)]
pub struct Whisky {
    pub distillery: String,
    pub slug: String,
    pub tastes: Tastes,
    pub correlations: Option<[Correlation; 9]>,
}

impl Whisky {
    fn from_csv_row(row: &StringRecord) -> Result<Self> {
        let distillery = distillery(row)?;
        let slug = Regex::new(r"[^a-z]+")
            .unwrap()
            .replace_all(distillery.to_lowercase().as_str(), "")
            .to_string();

        Ok(Self {
            distillery,
            slug,
            tastes: Tastes {
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
            },
            correlations: None,
        })
    }

    pub fn calculate_correlations(&mut self) -> Result<()> {
        let mut correlations: Vec<Correlation> = WHISKIES
            .par_iter()
            .filter(|w| w.distillery != self.distillery)
            .map(|w| Correlation::new(self, w))
            .collect::<Vec<Correlation>>();
        correlations.par_sort_by(|a, b| {
            if a.value > b.value {
                Ordering::Less
            } else if a.value < b.value {
                Ordering::Greater
            } else {
                Ordering::Equal
            }
        });
        let mut best = [
            correlations[0].clone(),
            correlations[1].clone(),
            correlations[2].clone(),
            correlations[3].clone(),
            correlations[4].clone(),
            correlations[5].clone(),
            correlations[6].clone(),
            correlations[7].clone(),
            correlations[8].clone(),
        ];
        best.par_iter_mut().try_for_each(|c| c.render_chart())?;
        self.correlations = Some(best);
        Ok(())
    }

    pub fn py(&self) -> PyWhisky {
        (
            self.distillery.clone(),
            self.slug.clone(),
            self.tastes.as_array(),
            self.correlations
                .clone()
                .map(|cs| cs.iter().map(|c| c.py()).collect::<Vec<PyCorrelation>>()),
        )
    }
}

fn whisky_by_name(name: String) -> Result<Whisky> {
    for w in WHISKIES.iter() {
        if w.distillery == name || w.slug == name {
            return Ok(w.clone());
        }
    }
    Err(anyhow!("Whisky {} not found", name))
}

pub fn recommendations_for(name: String) -> Result<PyWhisky> {
    let mut whisky = whisky_by_name(name)?;
    whisky.calculate_correlations()?;
    Ok(whisky.py())
}

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn test_all_whiskies_are_loaded() {
        assert_eq!(WHISKIES.len(), 86);
    }
}
