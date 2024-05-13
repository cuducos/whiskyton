use std::{collections::HashSet, f64::consts::PI};

use anyhow::Result;
use convert_case::{Case::Title, Casing};
use lazy_static::lazy_static;
use serde::Serialize;
use tera::{Context, Tera};

const WIDTH: u32 = 330;
const HEIGHT: u32 = 260;
const SIDES: u32 = 12;
const SCALES: u32 = 4;
const MARGIN: u32 = 60;
const TEXT_HEIGHT: f64 = 11.0;
const TASTES: [&str; 12] = [
    "body",
    "sweetness",
    "smoky",
    "medicinal",
    "tobacco",
    "honey",
    "spicy",
    "winey",
    "nutty",
    "malty",
    "fruity",
    "floral",
];

#[derive(Clone, Copy, Default, Debug, PartialEq, Serialize)]
struct Point {
    x: u32,
    y: u32,
}

type Area = [Point; 12];

type Grid = [Area; 4];

struct TextPositionAdjustments {
    bottom: HashSet<u32>,
    right: HashSet<u32>,
    top: HashSet<u32>,
    left: HashSet<u32>,
    diagonal_down: HashSet<u32>,
    diagonal_up: HashSet<u32>,
    sub_diagonal_down: HashSet<u32>,
}

#[derive(Debug, Serialize)]
struct Label {
    position: Point,
    text: String,
    align: String,
}

impl Label {
    fn new(order: u32) -> Self {
        let text_position_adjustments: TextPositionAdjustments = {
            TextPositionAdjustments {
                bottom: HashSet::from([0, 1]),
                right: HashSet::from([2, 3, 4, 5]),
                top: HashSet::from([6, 7]),
                left: HashSet::from([8, 9, 10, 11]),
                diagonal_down: HashSet::from([2, 11]),
                diagonal_up: HashSet::from([5, 8]),
                sub_diagonal_down: HashSet::from([3, 10]),
            }
        };
        let position = {
            let mut point = GRID[0][order as usize];
            if text_position_adjustments.top.contains(&order) {
                point.y = ((point.y as f64) - TEXT_HEIGHT * 0.75) as u32;
            }
            if text_position_adjustments.right.contains(&order) {
                point.x = (point.x as f64 + TEXT_HEIGHT * 0.75) as u32;
            }
            if text_position_adjustments.bottom.contains(&order) {
                point.y = (point.y as f64 + TEXT_HEIGHT * 1.5) as u32;
            }
            if text_position_adjustments.left.contains(&order) {
                point.x = (point.x as f64 - TEXT_HEIGHT * 0.75) as u32;
            }
            if text_position_adjustments.diagonal_up.contains(&order) {
                point.y = (point.y as f64 - TEXT_HEIGHT * 0.5) as u32;
            }
            if text_position_adjustments.diagonal_down.contains(&order) {
                point.y = (point.y as f64 + TEXT_HEIGHT * 0.75) as u32;
            }
            if text_position_adjustments.sub_diagonal_down.contains(&order) {
                point.y = (point.y as f64 + TEXT_HEIGHT * 0.25) as u32;
            }
            point
        };
        let align = {
            if text_position_adjustments.left.contains(&order) {
                "end"
            } else if text_position_adjustments.top.contains(&order)
                || text_position_adjustments.bottom.contains(&order)
            {
                "middle"
            } else {
                "start"
            }
            .to_string()
        };
        let text = TASTES[order as usize].to_string().to_case(Title);

        Self {
            position,
            text,
            align,
        }
    }
}

lazy_static! {
    static ref CENTER: Point = Point {
        x: WIDTH / 2,
        y: HEIGHT / 2
    };
    static ref GRID: Grid = {
        let width = WIDTH as f64;
        let height = HEIGHT as f64;
        let sides = SIDES as f64;

        let angle_adjust = (2.0 * PI / sides) / 2.0;
        let radius = (width - (2.0 * MARGIN as f64)) / 2.0;
        let interval = radius / SCALES as f64;

        let mut grid: Grid = Grid::default();
        for scale in 0..SCALES {
            let mut step: Area = Area::default();
            for side in 0..SIDES {
                let angle = ((2.0 * PI / sides) * side as f64) - angle_adjust;
                let r = radius - (scale as f64 * interval);
                let x = (width / 2.0) + (angle.sin() * r);
                let y = (height / 2.0) + (angle.cos() * r);
                step[side as usize] = Point {
                    x: x as u32,
                    y: y as u32,
                };
            }
            grid[scale as usize] = step;
        }
        grid
    };
    static ref LABELS: [Label; 12] = (0..12)
        .map(Label::new)
        .collect::<Vec<Label>>()
        .try_into()
        .unwrap();
    static ref TEMPLATE: Tera = {
        let mut tera = Tera::default();
        tera.add_raw_template("chart", include_str!("templates/chart.svg"))
            .unwrap();
        tera
    };
}

fn area_for(tastes: [u32; 12]) -> Area {
    let mut area: Area = Area::default();
    for (idx, taste) in tastes.into_iter().enumerate() {
        let position = (taste as i32 - SCALES as i32).unsigned_abs();
        area[idx] = if position == SCALES {
            *CENTER
        } else {
            GRID[position as usize][idx]
        }
    }
    area
}

pub struct Chart {
    reference: Area,
    other: Area,
}

impl Chart {
    pub fn new(reference: [u32; 12], other: [u32; 12]) -> Self {
        Self {
            reference: area_for(reference),
            other: area_for(other),
        }
    }

    pub fn svg(&self) -> Result<String> {
        let mut ctx = Context::new();
        // TODO: why it does not accept ref to statics?
        let grid = *GRID;
        let center = *CENTER;
        let labels: Vec<Label> = LABELS
            .iter()
            .map(|l| Label {
                text: l.text.clone(),
                align: l.align.clone(),
                position: l.position,
            })
            .collect();

        ctx.insert("grid", &grid);
        ctx.insert("reference", &self.reference);
        ctx.insert("other", &self.other);
        ctx.insert("center", &center);
        ctx.insert("labels", &labels);
        Ok(TEMPLATE.render("chart", &ctx)?)
    }
}

#[cfg(test)]
mod tests {

    use std::fs::read_to_string;

    use super::*;

    #[test]
    fn test_grid() {
        let expected = [
            [
                Point { x: 137, y: 231 },
                Point { x: 192, y: 231 },
                Point { x: 239, y: 204 },
                Point { x: 266, y: 157 },
                Point { x: 266, y: 102 },
                Point { x: 239, y: 55 },
                Point { x: 192, y: 28 },
                Point { x: 137, y: 28 },
                Point { x: 90, y: 55 },
                Point { x: 63, y: 102 },
                Point { x: 63, y: 157 },
                Point { x: 90, y: 204 },
            ],
            [
                Point { x: 144, y: 206 },
                Point { x: 185, y: 206 },
                Point { x: 220, y: 185 },
                Point { x: 241, y: 150 },
                Point { x: 241, y: 109 },
                Point { x: 220, y: 74 },
                Point { x: 185, y: 53 },
                Point { x: 144, y: 53 },
                Point { x: 109, y: 74 },
                Point { x: 88, y: 109 },
                Point { x: 88, y: 150 },
                Point { x: 109, y: 185 },
            ],
            [
                Point { x: 151, y: 180 },
                Point { x: 178, y: 180 },
                Point { x: 202, y: 167 },
                Point { x: 215, y: 143 },
                Point { x: 215, y: 116 },
                Point { x: 202, y: 92 },
                Point { x: 178, y: 79 },
                Point { x: 151, y: 79 },
                Point { x: 127, y: 92 },
                Point { x: 114, y: 116 },
                Point { x: 114, y: 143 },
                Point { x: 127, y: 167 },
            ],
            [
                Point { x: 158, y: 155 },
                Point { x: 171, y: 155 },
                Point { x: 183, y: 148 },
                Point { x: 190, y: 136 },
                Point { x: 190, y: 123 },
                Point { x: 183, y: 111 },
                Point { x: 171, y: 104 },
                Point { x: 158, y: 104 },
                Point { x: 146, y: 111 },
                Point { x: 139, y: 123 },
                Point { x: 139, y: 136 },
                Point { x: 146, y: 148 },
            ],
        ];
        for step in 0..4 {
            for point in 0..12 {
                assert_eq!(GRID[step][point], expected[step][point]);
            }
        }
    }

    #[test]
    fn test_area_for() {
        let tastes = [2, 2, 3, 1, 0, 2, 2, 1, 1, 1, 1, 2];
        let expected: Area = [
            Point { x: 151, y: 180 },
            Point { x: 178, y: 180 },
            Point { x: 220, y: 185 },
            Point { x: 190, y: 136 },
            Point { x: 165, y: 130 },
            Point { x: 202, y: 92 },
            Point { x: 178, y: 79 },
            Point { x: 158, y: 104 },
            Point { x: 146, y: 111 },
            Point { x: 139, y: 123 },
            Point { x: 139, y: 136 },
            Point { x: 127, y: 167 },
        ];
        assert_eq!(area_for(tastes), expected);
    }

    #[test]
    fn test_chart_renders() {
        let chart = Chart::new(
            [2, 2, 3, 1, 0, 2, 2, 1, 1, 1, 1, 2],
            [2, 3, 2, 0, 0, 2, 2, 1, 1, 2, 0, 1],
        );
        let expected = read_to_string("test_data/chart.sample.svg").unwrap();
        assert_eq!(expected, chart.svg().unwrap());
    }
}
