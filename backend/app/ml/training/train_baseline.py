from pathlib import Path
from time import perf_counter

import joblib
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

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models" / "intrusion_detection"

TRAIN_FILE = DATA_DIR / "train.csv"
TEST_FILE = DATA_DIR / "test.csv"

MODEL_FILE = MODEL_DIR / "random_forest_baseline.joblib"


def load_data():
    print("Loading training data...")

    train = pd.read_csv(TRAIN_FILE)
    test = pd.read_csv(TEST_FILE)

    feature_columns = [
        column
        for column in train.columns
        if column not in ["label", "target"]
    ]

    X_train = train[feature_columns]
    y_train = train["target"]

    X_test = test[feature_columns]
    y_test = test["target"]

    return X_train, X_test, y_train, y_test, feature_columns


def build_pipeline():
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
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    X_train, X_test, y_train, y_test, feature_columns = load_data()

    print(f"Training samples: {len(X_train):,}")
    print(f"Testing samples:  {len(X_test):,}")
    print(f"Features:         {len(feature_columns)}")

    print("\nBuilding model...")

    pipeline = build_pipeline()

    print("Training Random Forest...")

    start = perf_counter()

    pipeline.fit(X_train, y_train)

    elapsed = perf_counter() - start

    print(f"Training completed in {elapsed:.2f} seconds.")

    print("\nEvaluating model...")

    predictions = pipeline.predict(X_test)

    probabilities = pipeline.predict_proba(X_test)[:, 1]

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

    matrix = confusion_matrix(y_test, predictions)

    print(matrix)

    print("\nROC-AUC:")
    print(f"{roc_auc_score(y_test, probabilities):.4f}")

    joblib.dump(
        {
            "pipeline": pipeline,
            "feature_columns": feature_columns,
        },
        MODEL_FILE,
    )

    print("\nModel saved to:")
    print(MODEL_FILE)


if __name__ == "__main__":
    main()