use itertools::Itertools;

use crate::{feature, feature::Feature, logical_types::LogicalTypes, primitive::Primitive};

use super::generate_feature_sets;

pub fn generate_features_for_primitives<'a>(
    primitive: &'a Primitive,
    features: &'a Vec<Feature>,
) -> Vec<Feature> {
    // TODO: I think I need all the input types, and I'm just getting lucky here
    let inputset = &primitive.input_types[0];

    // a primitive may have multiple input types, so we need to generate all the possible combinations of
    // featureset for this input type
    let featuresets = generate_feature_sets(features, inputset, primitive.commutative);

    let mut new_features: Vec<Feature> = Vec::new();

    for featureset in featuresets {
        let base_features: Vec<Feature> = featureset.iter().map(|x| x.clone()).cloned().collect();

        let name: String = featureset
            .iter()
            .map(|x| &x.name)
            .cloned()
            .collect_vec()
            .join("_");
        // if primitive.commutative {
        //     base_features.sort();
        // }

        let name = format!("{}_{}", primitive.name, name);

        // let new_feature = feature!(name, primitive.clone());

        let new_feature = Feature::new(name, None, Some(primitive.clone()), Some(base_features));
        // let mut new_feature = Feature::new(
        //     primitive
        //         .return_type
        //         .logical_type
        //         .unwrap_or(LogicalTypes::Any),
        //     primitive
        //         .return_type
        //         .semantic_tag
        //         .unwrap_or(LogicalTypes::Any),
        //     Some(base_features),
        //     None,
        // );

        // new_feature.generating_primitive = Some(primitive.name.to_string());

        new_features.push(new_feature);
    }

    return new_features;
}
