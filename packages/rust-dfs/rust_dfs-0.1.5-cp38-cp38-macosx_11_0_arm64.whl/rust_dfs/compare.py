import json


def compare_rust_to_ft(ft_fname="all_features.json", rust_fname="rust_features.json"):
    ft_features = json.load(open(ft_fname))
    ft_features = [x["name"] for x in ft_features]
    ft_features = set([x for x in ft_features if x != "PrimitiveBase_"])

    rust_features = json.load(open(rust_fname))
    rust_features = set([x["name"] for x in rust_features])

    features_in_rust_that_arent_in_ft = rust_features - ft_features

    print("Set(Rust) - Set(FT)", features_in_rust_that_arent_in_ft)

    features_in_ft_that_arent_in_rust = ft_features - rust_features
    print("Set(FT) - Set(Rust)", features_in_ft_that_arent_in_rust)
