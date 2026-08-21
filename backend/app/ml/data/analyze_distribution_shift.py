from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[4]

RAW_DIR = PROJECT_ROOT / "data" / "raw"

TUESDAY_FILE = RAW_DIR / "Tuesday-WorkingHours.pcap_ISCX.csv"
WEDNESDAY_FILE = RAW_DIR / "Wednesday-workingHours.pcap_ISCX.csv"


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    df = df.replace([np.inf, -np.inf], np.nan)

    return df


def main():
    print("Loading datasets...")

    tuesday = load_dataset(TUESDAY_FILE)
    wednesday = load_dataset(WEDNESDAY_FILE)

    feature_columns = [
        column
        for column in tuesday.columns
        if column != "label"
    ]

    print(f"Features analysed: {len(feature_columns)}")

    results = []

    for feature in feature_columns:

        tuesday_median = tuesday[feature].median()
        wednesday_median = wednesday[feature].median()

        tuesday_mean = tuesday[feature].mean()
        wednesday_mean = wednesday[feature].mean()

        if pd.isna(tuesday_mean) or pd.isna(wednesday_mean):
            continue

        pooled_std = np.sqrt(
            (
                tuesday[feature].var()
                + wednesday[feature].var()
            ) / 2
        )

        if pooled_std == 0:
            effect_size = 0
        else:
            effect_size = abs(
                tuesday_mean - wednesday_mean
            ) / pooled_std

        results.append(
            {
                "feature": feature,
                "tuesday_mean": tuesday_mean,
                "wednesday_mean": wednesday_mean,
                "tuesday_median": tuesday_median,
                "wednesday_median": wednesday_median,
                "effect_size": effect_size,
            }
        )

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "effect_size",
        ascending=False,
    )

    print("\nTop 20 features with distribution shift:")
    print(
        results_df.head(20).to_string(index=False)
    )

    output_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "distribution_shift.csv"
    )

    results_df.to_csv(
        output_file,
        index=False,
    )

    print(f"\nSaved analysis to:")
    print(output_file)


if __name__ == "__main__":
    main()