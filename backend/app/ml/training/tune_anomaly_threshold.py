from pathlib import Path

import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
)


PROJECT_ROOT = Path(__file__).resolve().parents[4]

SCORES_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "anomaly_scores.csv"
)


def main():
    print("Loading anomaly scores...")

    df = pd.read_csv(SCORES_FILE)

    y_true = df["label"]
    scores = df["score"]

    thresholds = [
        -0.15,
        -0.10,
        -0.05,
        0.00,
        0.02,
        0.04,
        0.06,
        0.08,
        0.10,
    ]

    results = []

    for threshold in thresholds:

        predictions = (
            scores >= threshold
        ).astype(int)

        precision = precision_score(
            y_true,
            predictions,
            zero_division=0,
        )

        recall = recall_score(
            y_true,
            predictions,
            zero_division=0,
        )

        f1 = f1_score(
            y_true,
            predictions,
            zero_division=0,
        )

        false_positives = (
            ((y_true == 0) & (predictions == 1))
            .sum()
        )

        false_positive_rate = (
            false_positives
            / (y_true == 0).sum()
        )

        results.append(
            {
                "threshold": threshold,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "false_positives": false_positives,
                "false_positive_rate": false_positive_rate,
            }
        )

    results_df = pd.DataFrame(results)

    print("\nThreshold comparison:")
    print(
        results_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    best = results_df.loc[
        results_df["f1"].idxmax()
    ]

    print("\nBest F1 threshold:")
    print(
        f"Threshold: {best['threshold']:.4f}"
    )
    print(
        f"Precision: {best['precision']:.4f}"
    )
    print(
        f"Recall: {best['recall']:.4f}"
    )
    print(
        f"F1: {best['f1']:.4f}"
    )


if __name__ == "__main__":
    main()