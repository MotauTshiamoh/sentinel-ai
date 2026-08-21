from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = PROJECT_ROOT / "data" / "raw"


def inspect_file(filename: str) -> None:
    file_path = DATA_DIR / filename

    print("=" * 80)
    print(f"FILE: {filename}")
    print("=" * 80)

    df = pd.read_csv(file_path)

    print(f"\nRows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn names:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    missing = df.isnull().sum()
    print(missing[missing > 0].sort_values(ascending=False))

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nLast column / label distribution:")
    print(df.iloc[:, -1].value_counts(dropna=False))


if __name__ == "__main__":
    files = [
        "Tuesday-WorkingHours.pcap_ISCX.csv",
        "Wednesday-workingHours.pcap_ISCX.csv",
    ]

    for filename in files:
        inspect_file(filename)