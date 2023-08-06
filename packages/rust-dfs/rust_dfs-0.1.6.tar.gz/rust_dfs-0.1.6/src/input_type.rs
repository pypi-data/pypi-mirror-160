use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

use crate::logical_types::LogicalTypes;

#[pyclass]
#[derive(Debug, PartialEq, Eq, Deserialize, Serialize, Clone, Hash)]
pub struct InputType {
    pub logical_type: Option<LogicalTypes>,
    pub semantic_tag: Option<LogicalTypes>,
}

impl InputType {
    pub fn new(
        logical_type: Option<LogicalTypes>,
        semantic_tag: Option<LogicalTypes>,
    ) -> InputType {
        InputType {
            logical_type,
            semantic_tag,
        }
    }
}

#[pymethods]
impl InputType {
    #[new]
    pub fn __init__(lt: Option<&str>, st: Option<&str>) -> Self {
        InputType {
            logical_type: match lt {
                Some(lt) => Some(
                    LogicalTypes::try_from(lt)
                        .expect(format!("{} is not a valid logical type", lt).as_str()),
                ),
                None => None,
            },
            semantic_tag: match st {
                Some(lt) => Some(
                    LogicalTypes::try_from(lt)
                        .expect(format!("{} is not a valid logical type", lt).as_str()),
                ),
                None => None,
            },
        }
    }
    fn __str__(&self) -> PyResult<String> {
        Ok(format!("{:?}:{:?}", self.logical_type, self.semantic_tag))
    }
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("{:?}:{:?}", self.logical_type, self.semantic_tag))
    }
}

#[macro_export]
macro_rules! input_type {
    ($lt:expr, $st:expr) => {{
        use crate::input_type::InputType;
        use crate::logical_types::LogicalTypes;

        let lt = match LogicalTypes::try_from($lt) {
            Ok(x) => Some(x),
            Err(_) => None,
        };

        let st = match LogicalTypes::try_from($st) {
            Ok(x) => Some(x),
            Err(_) => None,
        };

        InputType::new(lt, st)
    }};
}
#[cfg(test)]
mod tests {

    use super::InputType;

    #[test]
    fn test_macro() {
        let b = input_type!["integer", "numeric"];

        println!("{:?}", b);
    }
}
