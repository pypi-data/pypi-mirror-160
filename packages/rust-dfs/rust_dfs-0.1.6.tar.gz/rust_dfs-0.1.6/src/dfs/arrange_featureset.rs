use std::collections::HashMap;

use crate::{feature::Feature, logical_types::LogicalTypes};

pub fn arrange_featureset<'a>(
    featureset: Vec<(&LogicalTypes, &'a Feature)>,
    index_by_logical_type: &HashMap<&LogicalTypes, Vec<usize>>,
) -> Vec<&'a Feature> {
    let mut current_index_by_logical_type: HashMap<LogicalTypes, usize> = HashMap::new();

    let mut features_with_position: Vec<(usize, &Feature)> = Vec::new();
    for (lt, f) in featureset {
        let idx = current_index_by_logical_type.entry(*lt).or_insert(0);
        let idx2 = index_by_logical_type.get(&lt).unwrap().get(*idx).unwrap();
        *idx += 1;

        features_with_position.push((*idx2, f));
    }

    features_with_position.sort_by(|a, b| a.0.cmp(&b.0));

    return features_with_position
        .iter()
        .map(|(_, f)| f)
        .cloned()
        .collect();
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use crate::{feature::Feature, logical_types::LogicalTypes};

    use super::arrange_featureset;

    #[test]
    fn test_arrange_featureset() {
        // let (features, _) = setup();

        // let f: Vec<&Feature> = features.iter().collect();

        // let featuremap = HashMap::from([
        //     (LogicalTypes::Boolean, vec![f[0], f[2]]),
        //     (LogicalTypes::BooleanNullable, vec![f[1]]),
        // ]);

        // let inputset = vec![
        //     LogicalTypes::Boolean,
        //     LogicalTypes::BooleanNullable,
        //     LogicalTypes::Boolean,
        // ];

        // let actual = arrange_featureset(featuremap, inputset);

        // assert_eq!(actual, f);
    }

    #[test]
    fn test_arrange_featureset2() {
        // input_set = [Boolean, Integer, Boolean]
        let index_by_logical_type: HashMap<&LogicalTypes, Vec<usize>> = HashMap::from([
            (&LogicalTypes::Boolean, vec![0, 2]),
            (&LogicalTypes::Integer, vec![1]),
        ]);

        // TODO: Fix this
        // let f1 = Feature::new(
        //     "F1".to_string(),
        //     LogicalTypes::Boolean,
        //     LogicalTypes::Categorical,
        //     None,
        //     None,
        // );
        // let f2 = Feature::new(
        //     "F2".to_string(),
        //     LogicalTypes::Boolean,
        //     LogicalTypes::Categorical,
        //     None,
        //     None,
        // );
        // let f3 = Feature::new(
        //     "F3".to_string(),
        //     LogicalTypes::Boolean,
        //     LogicalTypes::Categorical,
        //     None,
        //     None,
        // );

        // let featureset: Vec<(&LogicalTypes, &Feature)> = vec![
        //     (&LogicalTypes::Boolean, &f1),
        //     (&LogicalTypes::Boolean, &f2),
        //     (&LogicalTypes::Integer, &f3),
        // ];

        // let expected = vec![&f1, &f3, &f2];

        // let actual = arrange_featureset(featureset, &index_by_logical_type);

        // assert_eq!(actual, expected);
    }
}
