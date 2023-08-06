use crate::{feature::Feature, logical_types::LogicalTypes};
use itertools::Itertools;

pub fn generate_combinations<'a>(
    features: Vec<(&'a LogicalTypes, &'a Feature)>,
    n: usize,
    is_commutative: bool,
) -> Vec<Vec<(&LogicalTypes, &'a Feature)>> {
    if is_commutative {
        features.iter().cloned().combinations(n).collect_vec()
    } else {
        features.iter().cloned().permutations(n).collect_vec()
    }
}

#[cfg(test)]
mod tests {
    use super::generate_combinations;
    use crate::{feature, feature::Feature, input_type, logical_types::LogicalTypes, primitive};
    #[test]
    fn test_generate_combinations() {
        let p = primitive!(
            "Identity",
            vec![],
            input_type!["boolean", "categorical"],
            false
        );

        let fa_1 = feature!("FA_1", p.clone());
        let fa_2 = feature!("FA_2", p.clone());
        let fa_3 = feature!("FA_3", p.clone());

        let features = vec![
            (&LogicalTypes::Boolean, &fa_1),
            (&LogicalTypes::Boolean, &fa_2),
            (&LogicalTypes::Boolean, &fa_3),
        ];
        let actual = generate_combinations(features, 2, true);

        let expected = vec![
            vec![
                (&LogicalTypes::Boolean, &fa_1),
                (&LogicalTypes::Boolean, &fa_2),
            ],
            vec![
                (&LogicalTypes::Boolean, &fa_1),
                (&LogicalTypes::Boolean, &fa_3),
            ],
            vec![
                (&LogicalTypes::Boolean, &fa_2),
                (&LogicalTypes::Boolean, &fa_3),
            ],
        ];

        assert_eq!(actual, expected);
    }
}
