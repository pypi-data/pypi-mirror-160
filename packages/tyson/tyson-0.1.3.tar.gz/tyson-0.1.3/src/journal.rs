use crate::de::Desereilize;
use crate::item::{Item, ItemStruct};
use crate::primitive::PrimitiveItem;
use pyo3::prelude::*;

#[derive(Debug)]
#[pyclass]
pub struct Document {
    #[pyo3(get)]
    items: Vec<(PrimitiveItem, ItemStruct)>,
}

impl Desereilize for Document {
    fn new() -> Document {
        Document {
            items: vec![]
        }
    }

    fn push(&mut self, data: (PrimitiveItem, ItemStruct)) {
        self.items.push(data)
    }
}

// #[pymethods]
// impl Document {
//     #[get_items]
//     fn get_items(&self) {}
// }