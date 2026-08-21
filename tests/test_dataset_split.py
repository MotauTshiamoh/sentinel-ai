from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def test_train_and_test_have_no_duplicate_rows():
    train = pd.read_csv(PROCESSED_DIR / "train.csv")
    test = pd.read_csv(PROCESSED_DIR / "test.csv")

    train_features = train.drop(columns=["label", "target"])
    test_features = test.drop(columns=["label", "target"])

    train_hashes = pd.util.hash_pandas_object(
        train_features,
        index=False
    )

    test_hashes = pd.util.hash_pandas_object(
        test_features,
        index=False
    )

    overlap = set(train_hashes).intersection(set(test_hashes))

    assert len(overlap) == 0