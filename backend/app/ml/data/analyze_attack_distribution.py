from pathlib import Path

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

    df["label"] = df["label"].str.strip()

    return df


def analyse(name: str, df: pd.DataFrame):
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    print(f"Total rows: {len(df):,}")

    print("\nAttack distribution:")

    counts = df["label"].value_counts()

    percentages = (
        df["label"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
    )

    result = pd.DataFrame(
        {
            "count": counts,
            "percentage": percentages,
        }
    )

    print(result)


def main():
    print("Loading datasets...")

    tuesday = load_dataset(TUESDAY_FILE)
    wednesday = load_dataset(WEDNESDAY_FILE)

    analyse("TUESDAY", tuesday)
    analyse("WEDNESDAY", wednesday)


if __name__ == "__main__":
    main()