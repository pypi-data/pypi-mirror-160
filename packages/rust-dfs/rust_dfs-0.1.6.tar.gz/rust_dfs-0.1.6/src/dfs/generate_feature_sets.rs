use crate::{
    dfs::arrange_featureset::arrange_featureset,
    feature::{get_features_by_type, Feature},
    input_set::InputSet,
    logical_types::LogicalTypes,
};
use itertools::Itertools;
use std::collections::{HashMap, HashSet};

use super::{generate_combinations, index_input_set};

/// Generates a vector of featuresets for a given primitive.
///
/// For example, lets represent a feature as F1::A, this is a feature
/// with the name F1 and has a logical type of A.
///
/// If the the input features set is [F1::A, F2::A, F3::B, F4::A, F5::A], and the primitive has
/// a signature of [A,B,A], the possible output featuresets are:
///
/// [
///     [F1::A, F3::B, F2::A],
///     [F1::A, F3::B, F4::A],
///     [F2::A, F3::B, F4::A],
///     [F1::A, F5::B, F2::A],
///     [F1::A, F5::B, F4::A],
///     [F2::A, F5::B, F4::A],
/// ]
///
pub fn generate_feature_sets<'a>(
    features: &'a Vec<Feature>,
    input_set: &'a InputSet,
    is_commutative: bool,
) -> Vec<Vec<&'a Feature>> {
    // index input_set by logical_type
    let input_type_categories: HashMap<&LogicalTypes, Vec<usize>> = index_input_set(input_set);

    // let input_type_categories2: HashMap<LogicalTypes, Vec<usize>> = index_input_set(input_set);

    // find all the features that are of the same logical_type
    let features_by_type: HashMap<LogicalTypes, HashSet<&Feature>> = get_features_by_type(features);

    // let mut my_map = HashMap::new();

    let mut feature_combinations_for_type = Vec::new();

    for (&key, value) in &input_type_categories {
        // the number of inputs of this type
        let n_inputs = value.len();

        // Get all Features for this logical_type
        // https://blog.tawhidhannan.co.uk/rust/tidbits/rust-double-ref/
        let features_for_type = features_by_type
            .get(&key)
            .unwrap_or(&HashSet::new())
            .iter()
            .cloned()
            .map(|f| (key, f))
            .collect_vec();

        let perms = generate_combinations(features_for_type, n_inputs, is_commutative);

        // // NOTE: why does cloned here work?
        // // without cloned I get: does not live long enough:  Vec<(LogicalTypes, &Vec<&Feature>)>
        // // with cloned it works perms2: Vec<(LogicalTypes, Vec<&Feature>)>
        // let perms2 = perms.iter().cloned().map(|x| (key, x)).collect_vec();

        // my_map.insert(key, perms2);
        feature_combinations_for_type.push(perms);
    }

    // println!("{:#?}", my_map);

    // let a = my_map.values().cloned().collect_vec();

    let combinations_product = feature_combinations_for_type
        .iter()
        .cloned()
        .multi_cartesian_product()
        .map(|x| x.iter().flatten().cloned().collect_vec())
        .map(|x| arrange_featureset(x, &input_type_categories))
        .collect_vec();

    // println!("{:#?}", combinations_product);

    // todo!()

    return combinations_product;
    // let mut t: Vec<HashMap<LogicalTypes, Vec<&Feature>>> = Vec::new();
    // for h in f {
    //     let mut g: HashMap<LogicalTypes, Vec<&Feature>> = HashMap::new();
    //     for (lt, fs) in h {
    //         g.insert(lt.clone(), fs);
    //     }
    //     t.push(g);
    // }

    // let mut f_out = Vec::new();
    // for f in &t {
    //     let lts = input_set
    //         .iter()
    //         .map(|x| {
    //             if x.logical_type.is_some() {
    //                 x.logical_type.unwrap()
    //             } else if x.semantic_tag.is_some() {
    //                 x.semantic_tag.unwrap()
    //             } else {
    //                 LogicalTypes::Any
    //             }
    //         })
    //         .collect_vec();
    //     let a = arrange_featureset(f.clone(), lts);

    //     f_out.push(a)
    // }

    // return f_out;
}

#[cfg(test)]
mod tests {

    use std::collections::HashSet;

    use crate::{
        feature, feature::Feature, input_set::InputSet, input_type::InputType,
        logical_types::LogicalTypes,
    };

    use super::generate_feature_sets;

    #[test]
    fn test_generate_feature_sets() {
        let inputset = InputSet::new(vec![
            InputType::new(Some(LogicalTypes::Boolean), Some(LogicalTypes::Categorical)),
            InputType::new(Some(LogicalTypes::Integer), Some(LogicalTypes::Numeric)),
            InputType::new(Some(LogicalTypes::Boolean), Some(LogicalTypes::Categorical)),
        ]);

        let f1 = feature!("F1", "boolean", "categorical");
        let f2 = feature!("F2", "boolean", "categorical");
        let f3 = feature!("F3", "integer", "numeric");
        let f4 = feature!("F4", "boolean", "categorical");
        let f5 = feature!("F5", "integer", "numeric");

        let features: &Vec<Feature> =
            &vec![f1.clone(), f2.clone(), f3.clone(), f4.clone(), f5.clone()];

        let expected = HashSet::from([
            "F1_F3_F2", "F2_F3_F1", "F1_F3_F4", "F4_F3_F1", "F2_F3_F4", "F4_F3_F2", "F1_F5_F2",
            "F2_F5_F1", "F1_F5_F4", "F4_F5_F1", "F2_F5_F4", "F4_F5_F2",
        ]);

        let actual = generate_feature_sets(features, &inputset, false);

        let actual_str: Vec<String> = actual
            .iter()
            .map(|x| {
                let names: Vec<String> = x.iter().map(|x| &x.name).cloned().collect();
                return names.join("_");
            })
            .collect();

        for a in actual_str {
            assert!(expected.contains(&a[..]));
        }
    }
}
