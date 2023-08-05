import pandas as pd
import featuretools as ft
import json
from featuretools.primitives.utils import (
    get_aggregation_primitives,
    get_transform_primitives,
)
from .rust_dfs import Primitive, Feature

tag_map = {
    "numeric": "Numeric",
    "category": "Categorical",
    "time_index": "TimeIndex",
    "foreign_key": "ForeignKey",
    "date_of_birth": "DateOfBirth",
    "index": "Index",
}


def convert_primitives(ft_primitives):
    out = []
    for fp in ft_primitives:
        fp_dict = serialize_primitive(fp(), "transform")

        # input_types = fp_dict["input_types"][0]
        input_types = []
        for y in fp_dict["input_types"]:
            input_types.append([(x["logical_type"], x["semantic_tag"]) for x in y])

        out.append(
            Primitive(
                fp_dict["type"],
                fp_dict["module"],
                "transform",
                fp_dict["commutative"],
                input_types,
                (
                    fp_dict["return_type"]["logical_type"],
                    fp_dict["return_type"]["semantic_tag"],
                ),
            )
        )
    return out


def dataframe_to_features(df):
    features = []
    for name, col in df.ww.schema.columns.items():
        col_dict = col_to_dict(col)
        f = Feature(
            name,
            col_dict["logical_type"],
            col_dict["semantic_tag"] if col_dict["semantic_tag"] else "Any",
        )

        features.append(f)
    return features


def convert_features(f_features):
    f_features = f_features.copy()

    all_features = {}
    while f_features:
        f = f_features.pop(0)

        if len(f.base_features) == 0:
            all_features[f._name] = convert_feature(f)
        elif all([x._name in all_features for x in f.base_features]):

            base_features = [all_features[x._name] for x in f.base_features]
            all_features[f._name] = convert_feature(f, base_features)
        else:
            for bf in f.base_features:
                if bf._name not in all_features:
                    f_features.append(bf)
            f_features.append(f)

    return all_features


def convert_feature(f_feature, base_features=[]):

    name = f_feature._name

    primitive = type(f_feature.primitive)

    primitive_name = primitive.__name__

    if primitive_name == "PrimitiveBase":
        primitive_name = None

    if len(base_features):
        b_name = "_".join([x.name for x in base_features])
        name = f"{primitive_name}_{b_name}"

    if hasattr(f_feature, "return_type"):
        col_dict = col_to_dict(f_feature.return_type)
    else:
        col_dict = col_to_dict(primitive.return_type)

    return Feature(
        name,
        col_dict["logical_type"] or "Any",
        col_dict["semantic_tag"] or "Any",
        base_features,
        primitive_name,
    )


def col_to_dict(col):
    if col.logical_type:
        lt_name = type(col.logical_type).__name__
    else:
        lt_name = None

    semantic_tags = list(col.semantic_tags)

    if len(semantic_tags):
        semantic_tags = tag_map[semantic_tags[0]]
    else:
        semantic_tags = None
    return {
        "logical_type": lt_name,
        "semantic_tag": semantic_tags,
    }


def get_input_types(input_types):
    if not isinstance(input_types[0], list):
        input_types = [input_types]

    out = []
    for input_type_set in input_types:
        out_set = []
        for input_type in input_type_set:
            out_set.append(col_to_dict(input_type))
        out.append(out_set)
    return out


def serialize_primitive(primitive, function_type):
    """build a dictionary with the data necessary to construct the given primitive"""
    args_dict = {name: val for name, val in primitive.get_arguments()}
    cls = type(primitive)

    if primitive.return_type is None:
        return_type = primitive.input_types[0]
    else:
        return_type = primitive.return_type
    return {
        "type": cls.__name__,
        "module": cls.__module__,
        "arguments": args_dict,
        "input_types": get_input_types(primitive.input_types),
        "return_type": col_to_dict(return_type),
        "function_type": function_type,
        "commutative": primitive.commutative,
    }


def bool_column(nrows, start_idx=0, n_features=5):
    data = {}
    for n in range(n_features):
        name = f"F_{start_idx + n}"
        data[name] = [True] * nrows
    return pd.DataFrame(data)


def integer_column(nrows, start_idx=0, n_features=5):
    data = {}
    for n in range(n_features):
        name = f"F_{start_idx + n}"
        data[name] = [1] * nrows
    return pd.DataFrame(data)


def generate_fake_dataframe(n_rows=10, col_defs=[("Integer", 2)]):

    dataframes = [pd.DataFrame({"idx": range(n_rows)})]

    starting_col = 0
    for typ, n_cols in col_defs:
        if typ == "Integer":
            dataframes.append(integer_column(n_rows, starting_col, n_cols))
        elif typ == "Boolean":
            dataframes.append(bool_column(n_rows, starting_col, n_cols))

        starting_col += n_cols

    return pd.concat(dataframes, axis=1)


def df_to_es(df):
    es = ft.EntitySet(id="nums")
    es.add_dataframe(df, "nums", index="idx")

    return es


def serialize_feature(f):
    base_features = [x._name for x in f.base_features]
    cls = type(f.primitive)
    primitive_name = cls.__name__
    n2 = "_".join(base_features)

    return {
        "name": f"{primitive_name}_{n2}",
        "base_features": base_features,
        "generating_primitive": primitive_name,
        "commutative": cls.commutative,
    }


def save_features(features, fname="all_features.json"):
    out = []
    for f in features:
        out.append(serialize_feature(f))

    json.dump(out, open(fname, "w"))


def serialize_all_primitives():
    transform_prim_dict = get_transform_primitives()
    aggregation_prim_dict = get_aggregation_primitives()

    trans_prims = list(transform_prim_dict.values())

    agg_prims = list(aggregation_prim_dict.values())

    all_prims = []

    for p in trans_prims:
        all_prims.append(serialize_primitive(p(), "transform"))

    for p in agg_prims:
        all_prims.append(serialize_primitive(p(), "aggregation"))

    json.dump(all_prims, open("primitives.json", "w"))
