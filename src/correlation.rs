use anyhow::Result;

use crate::{chart::Chart, whisky::Whisky};

pub fn pearson_r(x: [u32; 12], y: [u32; 12]) -> f64 {
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
        num / den
    } else {
        0.0
    }
}

pub type PyCorrelation = (f64, String, Option<String>);

#[derive(Clone)]
pub struct Correlation {
    pub value: f64,
    pub whisky: String,
    pub chart: Option<String>,

    reference: [u32; 12],
    other: [u32; 12],
}

impl Correlation {
    pub fn new(whisky: &Whisky, other_whisky: &Whisky) -> Self {
        let reference = whisky.tastes.as_array();
        let other = other_whisky.tastes.as_array();

        Self {
            value: pearson_r(reference, other),
            whisky: other_whisky.distillery.clone(),
            chart: None,
            reference,
            other,
        }
    }

    pub fn render_chart(&mut self) -> Result<()> {
        let chart = Chart::new(self.reference, self.other);
        self.chart = Some(chart.svg()?);
        Ok(())
    }

    pub fn py(&self) -> PyCorrelation {
        (
            self.value,
            self.whisky.clone(),
            self.chart.clone(),
        )
    }
}

#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    fn test_pearson_r() {
        let expected = 0.7904333328627509;
        let x = [2, 2, 3, 1, 0, 2, 2, 1, 1, 1, 1, 2];
        let y = [2, 2, 3, 1, 0, 2, 1, 1, 1, 2, 1, 1];
        assert_eq!(pearson_r(x, y), expected);
    }
}
