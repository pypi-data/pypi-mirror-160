use pyo3::prelude::*;
use pyo3::pyclass::CompareOp;
use serde::{Deserialize, Serialize};
use std::cmp::Ordering;
use std::fs::{read_to_string, File};
use std::hash::{Hash, Hasher};
use std::io::prelude::*;
use std::{
    collections::{HashMap, HashSet},
    fmt,
};

use crate::input_type::InputType;
use crate::logical_types::LogicalTypes;
use crate::primitive::Primitive;
use crate::{input_type, primitive};

#[pyclass]
#[derive(Debug, Eq, Deserialize, Serialize, Clone)]
pub struct Feature {
    #[pyo3(get, set)]
    pub name: String,
    pub data_type: InputType,
    #[pyo3(get, set)]
    pub base_features: Vec<Feature>,
    pub generating_primitive: Option<Primitive>,
}

#[pymethods]
impl Feature {
    #[new]
    fn __init__(
        name: &str,
        lt: &str,
        st: &str,
        base_features: Option<Vec<Feature>>,
        generating_primitive: Option<Primitive>,
    ) -> Self {
        let lt = LogicalTypes::try_from(lt).ok();
        let st = LogicalTypes::try_from(st).ok();

        let dtype = InputType::new(lt, st);

        if base_features.is_some() ^ generating_primitive.is_some() {
            panic!("base_features and generating_primitive must be both None or both Some");
        }

        Feature::new(
            name.to_string(),
            Some(dtype),
            generating_primitive,
            base_features,
        )
    }
    fn __str__(&self) -> PyResult<String> {
        Ok(format!(
            "{}:{:?}:{:?}:{:?}",
            self.name,
            self.data_type,
            self.generating_primitive,
            self.base_features
                .iter()
                .map(|x| &x.name)
                .collect::<Vec<_>>()
        ))
    }
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!(
            "{}:{:?}:{:?}:{:?}",
            self.name,
            self.data_type,
            self.generating_primitive,
            self.base_features
                .iter()
                .map(|x| &x.name)
                .collect::<Vec<_>>()
        ))
    }

    fn __richcmp__(&self, other: &Feature, _op: CompareOp) -> PyResult<bool> {
        // println!("{:?} == {:?}", self, other);
        Ok(self.equals(other))
    }
}

impl Feature {
    pub fn new(
        name: String,
        data_type: Option<InputType>,
        generating_primitive: Option<Primitive>,
        base_features: Option<Vec<Feature>>,
    ) -> Feature {
        let dtype: InputType = if generating_primitive.is_some() {
            generating_primitive.as_ref().unwrap().clone().return_type
        } else {
            data_type.unwrap()
        };

        Feature {
            name,
            data_type: dtype,
            base_features: base_features.unwrap_or(vec![]),
            generating_primitive,
        }
    }

    pub fn equals(&self, other: &Feature) -> bool {
        // --> do I need this?
        self == other
    }

    pub fn write_many_to_file(features: &Vec<Feature>, filename: String) {
        let a = serde_json::to_string(&features);

        match a {
            Ok(s) => {
                // let filename = format!(&filename);
                let mut file = File::create(filename).unwrap();
                // let p = format!("{}\n", s);
                file.write_all(s.as_bytes()).expect("Error writing to file");
            }
            Err(e) => println!("{}", e),
        }
    }

    pub fn write_to_file(&self) {
        let j = serde_json::to_string(self);

        println!("--- FEATURE AS JSON");
        match j {
            Ok(s) => {
                println!("{}", s);
                let filename = format!("{}.json", self.name);
                let mut file = File::create(filename).unwrap();
                let p = format!("{}\n", s);
                file.write_all(p.as_bytes()).expect("Error writing to file");
            }
            Err(e) => println!("{}", e),
        }
    }

    pub fn read_from_file(filename: String) -> Feature {
        let contents = read_to_string(filename).expect("Something went wrong reading the file");
        let feature: Feature = serde_json::from_str(&contents[..]).unwrap();
        return feature;
    }
}

impl fmt::Display for Feature {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} : {:?}", self.name, self.data_type)
    }
}

impl Hash for Feature {
    fn hash<H: Hasher>(&self, state: &mut H) {
        match self.generating_primitive {
            Some(ref p1) => {
                p1.hash(state);

                let mut v = self.base_features.clone();
                v.sort();

                v.hash(state);
            }
            None => {
                self.name.hash(state);
            }
        }
    }
}

impl PartialOrd for Feature {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Feature {
    fn cmp(&self, other: &Self) -> Ordering {
        match (
            self.generating_primitive.clone(),
            other.generating_primitive.clone(),
        ) {
            (Some(ref p1), Some(ref p2)) => self.base_features.cmp(&other.base_features),
            _ => return self.name.cmp(&other.name),
        }
    }
}

impl PartialEq for Feature {
    fn eq(&self, other: &Self) -> bool {
        match (
            self.generating_primitive.clone(),
            other.generating_primitive.clone(),
        ) {
            (None, None) => self.name == other.name,
            (Some(ref p1), Some(ref p2)) => {
                if p1 != p2 {
                    return false;
                } else {
                    let bf = &self.base_features;
                    let other_bf = &other.base_features;

                    let is_commutative = self
                        .generating_primitive
                        .as_ref()
                        .unwrap()
                        .clone()
                        .commutative;

                    let bf_equal = match is_commutative {
                        true => {
                            let s1: HashSet<Feature> = HashSet::from_iter(bf.iter().cloned());
                            let s2: HashSet<Feature> = HashSet::from_iter(other_bf.iter().cloned());

                            println!("checking commutative equality");
                            s1 == s2
                        }
                        false => bf == other_bf,
                    };

                    return bf_equal;
                }
            }
            _ => return false,
        }
    }
}

pub fn get_features_by_type(features: &Vec<Feature>) -> HashMap<LogicalTypes, HashSet<&Feature>> {
    let mut features_by_type: HashMap<LogicalTypes, HashSet<&Feature>> = HashMap::new();

    for feature in features {
        let logical_type = feature.data_type.logical_type;

        if logical_type.is_some() {
            let features_of_type = features_by_type
                .entry(logical_type.unwrap())
                .or_insert(HashSet::new());
            features_of_type.insert(feature);
        }

        let semantic_type = feature.data_type.semantic_tag;

        if semantic_type.is_some() {
            let features_of_type = features_by_type
                .entry(semantic_type.unwrap())
                .or_insert(HashSet::new());
            features_of_type.insert(feature);
        }
    }

    features_by_type.insert(LogicalTypes::Any, HashSet::from_iter(features.iter()));

    return features_by_type;
}

#[macro_export]
macro_rules! feature {
    ($name:expr, $prim:expr, [$( $x:expr ),*] ) => {{
        let mut base_features: Vec<Feature> = Vec::new();
        $(
            base_features.push($x);
        )*

        Feature::new($name.to_string(), None, Some($prim), Some(base_features))
    }};
    ($name:expr, $prim:expr) => {{
        Feature::new($name.to_string(), None, Some($prim), None)
    }};
    ($name:expr, $lt:expr, $st:expr) => {{
        use crate::{input_type};
        let dtype = input_type![$lt, $st];
        Feature::new($name.to_string(), Some(dtype), None, None)
    }};
}

pub fn generate_fake_features(n_features: i32) -> Vec<Feature> {
    let p = primitive!("Identity", vec![], input_type!["integer", "numeric"], false);
    let mut features: Vec<Feature> = vec![feature!("idx", p)];

    for i in 0..(n_features - 1) {
        let name = format!("F_{}", i);
        // let logical_type = LogicalTypes::Integer;
        // let semantic_type = LogicalTypes::Numeric;
        // let base_features = None;
        // let feature = Feature::new(name, logical_type, semantic_type, base_features, None);
        features.push(feature!(name, "integer", "numeric"));
    }

    return features;
}

#[pyfunction]
pub fn compare_featuresets(
    features1: Vec<Feature>,
    features2: Vec<Feature>,
) -> (Vec<Feature>, Vec<Feature>) {
    let features1: HashSet<Feature> = HashSet::from_iter(features1.iter().cloned());

    let features2: HashSet<Feature> = HashSet::from_iter(features2.iter().cloned());

    let diff1: Vec<Feature> = features1.difference(&features2).cloned().collect();

    let diff2: Vec<Feature> = features2.difference(&features1).cloned().collect();

    return (diff1, diff2);
}

pub fn print_set(features: &Vec<Feature>) {
    println!("===");
    match features.len() {
        0 => println!("No difference"),
        _ => {
            println!("Features from s1 not in s2:");
            features.iter().for_each(|f| {
                println!("\t-> {}", f);
            });
        }
    }

    println!("===");
}

#[cfg(test)]
mod tests {
    use std::collections::HashSet;

    use crate::{
        feature::compare_featuresets, input_set, input_type, logical_types::LogicalTypes, primitive,
    };

    use super::Feature;

    #[test]
    fn test() {
        let p = primitive!("Identity", vec![], input_type!["integer", "numeric"], false);

        let f1 = feature!("idx", p.clone());
        let f2 = feature!("idx", p.clone());

        println!("Equal? {}", f1 == f2);
    }

    #[test]
    fn test_eq1() {
        let bf1 = feature!("bf1", "integer", "index");
        let bf1a = feature!("bf1", "integer", "index");
        let bf2 = feature!("bf2", "integer", "index");

        assert_eq!(bf1, bf1a);
        assert_ne!(bf1, bf2);

        assert_eq!([bf1.clone(), bf2.clone()], [bf1.clone(), bf2.clone()]);
        assert_ne!([bf1.clone(), bf2.clone()], [bf2.clone(), bf1.clone()]);

        let s1 = HashSet::from([&bf1, &bf1a, &bf2]);

        println!("{:?}", s1.contains(&bf1));
        println!("{:?}", s1.contains(&bf1a));
        assert!(s1.len() == 2);
    }

    #[test]
    fn test_eq2() {
        let bf1 = feature!("bf1", "integer", "index");
        let bf2 = feature!("bf2", "integer", "index");

        let inputs1 = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type1 = input_type!["integer", "numeric"];

        // Commutative is false, so order matters
        // result should be ["F1", "F3"], since "F2" is same as "F1"
        let p1 = primitive!("GreaterThan", inputs1, r_type1, false);

        let f1 = feature!("f1", p1.clone(), [bf1.clone(), bf2.clone()]);
        let f2 = feature!("f2", p1.clone(), [bf1.clone(), bf2.clone()]);
        let f3 = feature!("f3", p1.clone(), [bf2.clone(), bf1.clone()]);

        assert_eq!(f1, f2);
        assert_ne!(f1, f3);

        let s1 = HashSet::from([&f1, &f2, &f3]);

        // println!(
        //     "{:?}",
        //     s1.into_iter().map(|f| &f.name[..]).collect::<Vec<_>>()
        // );

        assert!(s1.len() == 2);

        // ================================================================

        let inputs2 = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type2 = input_type!["integer", "numeric"];

        let p2 = primitive!("GreaterThan", inputs2, r_type2, true);

        // Commutative is true, so order doesn't matter
        // result should be ["f1a"]
        let f1a = feature!("f1a", p2.clone(), [bf1.clone(), bf2.clone()]);
        let f2a = feature!("f2a", p2.clone(), [bf1.clone(), bf2.clone()]);
        let f3a = feature!("f3a", p2.clone(), [bf2.clone(), bf1.clone()]);

        let s2 = HashSet::from([&f1a, &f2a, &f3a]);

        // println!(
        //     "{:?}",
        //     s2.into_iter().map(|f| &f.name[..]).collect::<Vec<_>>()
        // );
        assert!(s2.len() == 1);
    }

    #[test]
    fn test_compare_featuresets() {
        let bf1 = feature!("bf1", "integer", "index");
        let bf2 = feature!("bf2", "integer", "index");
        let bf3 = feature!("bf3", "integer", "index");

        let inputs1 = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type1 = input_type!["integer", "numeric"];

        // Commutative is false, so order matters
        let p1 = primitive!("GreaterThan", inputs1, r_type1, false);

        let f1 = feature!("f1", p1.clone(), [bf1.clone(), bf2.clone()]);
        let f2 = feature!("f2", p1.clone(), [bf1.clone(), bf2.clone()]);
        let f3 = feature!("f2", p1.clone(), [bf2.clone(), bf1.clone()]);

        let (d1, d2) = compare_featuresets(vec![f1.clone()], vec![f2.clone()]);

        assert!(d1.len() == 0);
        assert!(d2.len() == 0);

        let (d1, d2) = compare_featuresets(vec![f1.clone()], vec![f3.clone()]);

        assert!(d1.len() == 1);
        assert!(d2.len() == 1);
    }

    #[test]
    fn test_macro() {
        let inputs = vec![
            input_set![["", "numeric"], ["", "numeric"]],
            input_set![["datetime", ""], ["datetime", ""]],
            input_set![["ordinal", ""], ["ordinal", ""]],
        ];

        let r_type = input_type!["integer", "numeric"];

        let p = primitive!("GreaterThan", inputs, r_type, false);

        let a = feature!("a", p.clone());
        let b = feature!("b", p.clone());

        let f1 = feature!("reed", p.clone(), [a, b]);
        let f2 = feature!("reed", p.clone());

        println!("{:?}", f1);
        println!("{:?}", f2);
    }
}
