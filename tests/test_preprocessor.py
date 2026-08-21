import pandas as pd

from app.ml.data.preprocessor import clean_column_names


def test_clean_column_names():
    df = pd.DataFrame(
        columns=[
            "Destination Port",
            "Flow Duration",
            "Total Fwd Packets"
        ]
    )

    cleaned = clean_column_names(df)

    assert list(cleaned.columns) == [
        "destination_port",
        "flow_duration",
        "total_fwd_packets"
    ]