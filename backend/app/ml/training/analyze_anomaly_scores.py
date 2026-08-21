from pathlib import Path

import joblib
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[4]

TEST_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Wednesday-workingHours.pcap_ISCX.csv"
)

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "intrusion_detection"
    / "isolation_forest.joblib"
)


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("/", "_")
    )

    df["label"] = df["label"].str.strip()

    return df


def main():
    print("Loading Wednesday test data...")

    df = load_dataset(TEST_FILE)

    y_true = (
        df["label"] != "BENIGN"
    ).astype(int)

    X = df.drop(columns=["label"])

    X = X.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    print("Loading Isolation Forest...")

    model = joblib.load(MODEL_FILE)

    print("Calculating anomaly scores...")

    scores = -model.decision_function(X)

    results = pd.DataFrame(
        {
            "label": y_true,
            "score": scores,
        }
    )

    print("\nAnomaly score statistics:")
    print(results["score"].describe())

    print("\nBENIGN score statistics:")
    print(
        results.loc[
            results["label"] == 0,
            "score"
        ].describe()
    )

    print("\nATTACK score statistics:")
    print(
        results.loc[
            results["label"] == 1,
            "score"
        ].describe()
    )

    output_file = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "anomaly_scores.csv"
    )

    results.to_csv(
        output_file,
        index=False,
    )

    print("\nScores saved to:")
    print(output_file)


if __name__ == "__main__":
    main()