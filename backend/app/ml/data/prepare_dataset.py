from pathlib import Path

import numpy as np
import pandas as pd

from app.ml.data.preprocessor import clean_column_names


PROJECT_ROOT = Path(__file__).resolve().parents[4]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


FILES = [
    "Tuesday-WorkingHours.pcap_ISCX.csv",
    "Wednesday-workingHours.pcap_ISCX.csv",
]


def load_and_combine() -> pd.DataFrame:
    frames = []

    for filename in FILES:
        file_path = RAW_DIR / filename

        print(f"Loading {filename}...")

        df = pd.read_csv(file_path)
        df = clean_column_names(df)

        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)

    return combined


def prepare_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove leading/trailing whitespace from labels
    df["label"] = df["label"].str.strip()

    # Convert infinite values to NaN
    df = df.replace([np.inf, -np.inf], np.nan)

    # Remove exact duplicate rows
    before = len(df)

    df = df.drop_duplicates()

    removed_exact = before - len(df)

    print(f"Removed exact duplicate rows: {removed_exact:,}")

    # Identify feature columns.
    # Label and target are excluded because we want to detect
    # identical network features with conflicting labels.
    feature_columns = [
        column
        for column in df.columns
        if column != "label"
    ]

    # Find feature vectors associated with more than one label.
    conflicting_features = (
        df.groupby(feature_columns, dropna=False)["label"]
        .nunique()
    )

    conflicting_features = conflicting_features[
        conflicting_features > 1
    ]

    print(
        "Conflicting feature vectors:",
        len(conflicting_features)
    )

    if len(conflicting_features) > 0:
        conflict_index = (
            df.set_index(feature_columns)
            .index.isin(conflicting_features.index)
        )

        removed_conflicts = conflict_index.sum()

        df = df.loc[~conflict_index].copy()

        print(
            "Removed rows with conflicting labels:",
            f"{removed_conflicts:,}"
        )

    # Create binary target
    df["target"] = (df["label"] != "BENIGN").astype(int)

    # Do NOT impute missing values here.
    # Missing-value handling will happen inside the ML pipeline
    # after the train/test split to prevent data leakage.

    return df

def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading datasets...")
    df = load_and_combine()

    print(f"\nCombined rows: {len(df):,}")
    print(f"Combined columns: {len(df.columns)}")

    print("\nPreparing dataset...")
    df = prepare_dataset(df)

    output_file = PROCESSED_DIR / "cicids2017_binary.csv"

    df.to_csv(output_file, index=False)

    print("\nDataset preparation complete.")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nOriginal labels:")
    print(df["label"].value_counts())

    print("\nBinary target:")
    print(df["target"].value_counts())

    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()