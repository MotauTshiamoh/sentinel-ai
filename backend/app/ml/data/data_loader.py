from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[4] / "data"


def load_csv(filename: str) -> pd.DataFrame:
    """
    Load a CSV dataset from the project's data directory.
    """
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)