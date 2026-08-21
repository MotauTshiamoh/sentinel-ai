import numpy as np

from pathlib import Path
from time import perf_counter

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[4]

RAW_DIR = PROJECT_ROOT / "data" / "raw"


TRAIN_FILE = RAW_DIR / "Tuesday-WorkingHours.pcap_ISCX.csv"
TEST_FILE = RAW_DIR / "Wednesday-workingHours.pcap_ISCX.csv"


def load_file(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    df["label"] = df["label"].str.strip()

    return df


def prepare(df: pd.DataFrame):
    df = df.replace([np.inf, -np.inf], np.nan)

    df["target"] = (df["label"] != "BENIGN").astype(int)

    feature_columns = [
        column
        for column in df.columns
        if column not in ["label", "target"]
    ]

    X = df[feature_columns]
    y = df["target"]

    return X, y, feature_columns


def build_model():
    return Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median"),
            ),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=100,
                    random_state=42,
                    n_jobs=-1,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def main():
    print("Loading Tuesday training data...")
    train_df = load_file(TRAIN_FILE)

    print("Loading Wednesday test data...")
    test_df = load_file(TEST_FILE)

    X_train, y_train, feature_columns = prepare(train_df)
    X_test, y_test, _ = prepare(test_df)

    print(f"\nTraining rows: {len(X_train):,}")
    print(f"Testing rows:  {len(X_test):,}")
    print(f"Features:      {len(feature_columns)}")

    print("\nTraining labels:")
    print(y_train.value_counts())

    print("\nTesting labels:")
    print(y_test.value_counts())

    model = build_model()

    print("\nTraining model...")
    start = perf_counter()

    model.fit(X_train, y_train)

    elapsed = perf_counter() - start

    print(f"Training completed in {elapsed:.2f} seconds.")

    print("\nEvaluating unseen day...")

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            target_names=["BENIGN", "ATTACK"],
            digits=4,
        )
    )

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    print("\nROC-AUC:")
    print(f"{roc_auc_score(y_test, probabilities):.4f}")


if __name__ == "__main__":
    main()