from pathlib import Path

import numpy as np
import pandas as pd
import joblib

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)


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

    print(f"Test rows: {len(df):,}")

    y_true = (
        df["label"] != "BENIGN"
    ).astype(int)

    X = df.drop(
        columns=["label"]
    )

    X = X.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    print("\nLoading Isolation Forest...")

    model = joblib.load(MODEL_FILE)

    print("Generating anomaly predictions...")

    # Isolation Forest:
    # -1 = anomaly
    #  1 = normal
    raw_predictions = model.predict(X)

    predictions = (
        raw_predictions == -1
    ).astype(int)

    # decision_function:
    # Lower values = more anomalous.
    anomaly_scores = -model.decision_function(X)

    print("\nClassification Report:")

    print(
        classification_report(
            y_true,
            predictions,
            target_names=[
                "BENIGN",
                "ATTACK",
            ],
            digits=4,
            zero_division=0,
        )
    )

    print("Confusion Matrix:")

    print(
        confusion_matrix(
            y_true,
            predictions,
        )
    )

    print("\nROC-AUC:")

    print(
        f"{roc_auc_score(y_true, anomaly_scores):.4f}"
    )

    print("\nPrediction distribution:")

    print(
        pd.Series(
            predictions
        ).value_counts()
        .rename(
            index={
                0: "BENIGN",
                1: "ANOMALY",
            }
        )
    )


if __name__ == "__main__":
    main()