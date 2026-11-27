import json
from pathlib import Path


def fetch_raw_bloomberg_history(
    identifier,
    start_date,
    end_date,
):
    path = Path("data/sample/bloomberg_reference_sample.json")

    with path.open() as file:
        data = json.load(file)

    for series in data["series"]:
        if series["provider_identifier"] == identifier:
            observations = [
                row for row in series["observations"]
                if start_date <= row["observation_date"] <= end_date
            ]
            return observations, series["canonical_ticker"]

    raise ValueError(f"No data found for {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    rows = []

    for row in raw_data:
        rows.append({
            "date": row["observation_date"],
            "ticker": canonical_ticker,
            "open": float(row["open_value"]),
            "high": float(row["high_value"]),
            "low": float(row["low_value"]),
            "close": float(row["close_value"]),
            "volume": int(row["volume_value"])
        })

    return rows