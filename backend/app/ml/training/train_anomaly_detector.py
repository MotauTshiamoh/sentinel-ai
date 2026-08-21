from pathlib import Path
from time import perf_counter

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[4]

TRAIN_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "train.csv"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "models"
    / "intrusion_detection"
)

MODEL_FILE = MODEL_DIR / "isolation_forest.joblib"


def main():
    print("Loading training data...")

    df = pd.read_csv(TRAIN_FILE)

    print(f"Training rows: {len(df):,}")

    # Train anomaly detector using BENIGN traffic only.
    benign = df[df["target"] == 0].copy()

    print(f"Benign training rows: {len(benign):,}")

    X = benign.drop(
        columns=["label", "target"]
    )

    # Replace infinite values with NaN.
    X = X.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    print(f"Features: {X.shape[1]}")

    model = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            ),
            (
                "model",
                IsolationForest(
                    n_estimators=100,
                    contamination=0.05,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print("\nTraining Isolation Forest...")

    start = perf_counter()

    model.fit(X)

    elapsed = perf_counter() - start

    print(
        f"Training completed in {elapsed:.2f} seconds."
    )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_FILE,
    )

    print("\nModel saved to:")
    print(MODEL_FILE)


if __name__ == "__main__":
    main()