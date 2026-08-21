from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[4]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


INPUT_FILE = PROCESSED_DIR / "cicids2017_binary.csv"

TRAIN_FILE = PROCESSED_DIR / "train.csv"
TEST_FILE = PROCESSED_DIR / "test.csv"


def main() -> None:
    print("Loading processed dataset...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Total rows: {len(df):,}")

    train_df, test_df = train_test_split(
        df,
        test_size=0.20,
        random_state=42,
        stratify=df["target"]
    )

    train_df.to_csv(TRAIN_FILE, index=False)
    test_df.to_csv(TEST_FILE, index=False)

    print("\nSplit complete.")

    print(f"Training rows: {len(train_df):,}")
    print(f"Testing rows:  {len(test_df):,}")

    print("\nTraining class distribution:")
    print(train_df["target"].value_counts())

    print("\nTesting class distribution:")
    print(test_df["target"].value_counts())

    print(f"\nTraining file: {TRAIN_FILE}")
    print(f"Testing file:  {TEST_FILE}")


if __name__ == "__main__":
    main()