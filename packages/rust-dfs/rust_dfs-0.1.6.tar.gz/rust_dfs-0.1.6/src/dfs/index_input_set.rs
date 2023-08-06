use std::collections::HashMap;

use crate::{input_set::InputSet, logical_types::LogicalTypes};

pub fn index_input_set(input_set: &InputSet) -> HashMap<&LogicalTypes, Vec<usize>> {
    let mut inputset_by_type: HashMap<&LogicalTypes, Vec<usize>> = HashMap::new();

    for (i, input) in input_set.iter().enumerate() {
        let lt = if input.logical_type.is_some() {
            let a = input.logical_type.as_ref().unwrap();
            a
        } else if input.semantic_tag.is_some() {
            let a = input.semantic_tag.as_ref().unwrap();
            a
        } else {
            &LogicalTypes::Any
        };

        let index_array_for_type = inputset_by_type.entry(lt).or_insert(Vec::new());

        index_array_for_type.push(i);
    }
    return inputset_by_type;
}

#[cfg(test)]
mod tests {
    use std::{collections::HashMap, vec};

    use crate::{input_set::InputSet, input_type::InputType, logical_types::LogicalTypes};

    use super::index_input_set;

    #[test]
    fn happy_path() {
        let input_set = InputSet::new(vec![
            InputType::new(Some(LogicalTypes::Boolean), None),
            InputType::new(Some(LogicalTypes::Integer), None),
            InputType::new(Some(LogicalTypes::Boolean), None),
        ]);

        let expected = HashMap::from([
            (&LogicalTypes::Boolean, vec![0, 2]),
            (&LogicalTypes::Integer, vec![1]),
        ]);

        let actual = index_input_set(&input_set);

        assert_eq!(expected, actual);
    }
}
