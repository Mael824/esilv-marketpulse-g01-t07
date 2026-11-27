import json
from pathlib import Path

ACCESS_MODE = "APPROVED_SAMPLE"

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

SAMPLE_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "sample"
    / "bloomberg_reference_sample.json"
)


def fetch_raw_bloomberg_history(identifier, start_date=None, end_date=None):
    """Raw input boundary. APPROVED_SAMPLE: read the approved fixture."""
    with open(SAMPLE_PATH, encoding="utf-8") as file:
        sample = json.load(file)

    for series in sample["series"]:
        if series["provider_identifier"] == identifier:
            observations = series["observations"]
            if start_date is not None:
                observations = [
                    o for o in observations if o["observation_date"] >= start_date
                ]
            if end_date is not None:
                observations = [
                    o for o in observations if o["observation_date"] <= end_date
                ]
            return observations

    raise ValueError(f"No approved sample series for {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    """Normalization boundary: teaching wrapper keys -> canonical rows."""
    rows = []
    for observation in raw_data:
        rows.append(
            {
                "date": observation["observation_date"],
                "ticker": canonical_ticker,
                "open": float(observation["open_value"]),
                "high": float(observation["high_value"]),
                "low": float(observation["low_value"]),
                "close": float(observation["close_value"]),
                "volume": int(observation["volume_value"]),
            }
        )
    return rows


def fetch_bloomberg_prices(canonical_ticker):
    """Canonical ticker in, canonical rows out."""
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_data = fetch_raw_bloomberg_history(identifier)
    rows = normalize_bloomberg_history(raw_data, canonical_ticker)
    if not rows:
        raise ValueError(f"No Bloomberg-stage rows for {canonical_ticker}")
    return rows