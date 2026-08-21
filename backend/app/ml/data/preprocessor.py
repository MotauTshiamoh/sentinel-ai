import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardise dataset column names.
    """
    cleaned = df.copy()

    cleaned.columns = (
        cleaned.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("/", "_")
    )

    return cleaned