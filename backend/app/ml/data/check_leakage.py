from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[4]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def main() -> None:
    train = pd.read_csv(PROCESSED_DIR / "train.csv")
    test = pd.read_csv(PROCESSED_DIR / "test.csv")

    feature_columns = [
        column
        for column in train.columns
        if column not in ["label", "target"]
    ]

    train_features = train[feature_columns]
    test_features = test[feature_columns]

    train_hashes = pd.util.hash_pandas_object(
        train_features,
        index=False
    )

    test_hashes = pd.util.hash_pandas_object(
        test_features,
        index=False
    )

    overlap = set(train_hashes).intersection(set(test_hashes))

    print(f"Duplicate feature rows across train/test: {len(overlap)}")

    if not overlap:
        return

    train["feature_hash"] = train_hashes
    test["feature_hash"] = test_hashes

    overlapping_train = train[
        train["feature_hash"].isin(overlap)
    ]

    overlapping_test = test[
        test["feature_hash"].isin(overlap)
    ]

    print("\nTRAIN labels:")
    print(overlapping_train["label"].value_counts())

    print("\nTEST labels:")
    print(overlapping_test["label"].value_counts())

    combined = pd.concat(
        [
            overlapping_train[["feature_hash", "label", "target"]],
            overlapping_test[["feature_hash", "label", "target"]],
        ]
    )

    print("\nOverlapping feature rows:")
    print(combined.sort_values("feature_hash").to_string(index=False))


if __name__ == "__main__":
    main()