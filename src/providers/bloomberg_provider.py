from pathlib import Path
import json

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}


def load_bloomberg_reference_sample():
    path = Path(__file__).resolve().parents[2]
    path = path / "data/sample/bloomberg_reference_sample.json"

    with open(path, encoding="utf-8") as file:
        return json.load(file)


def find_reference_series(payload, provider_identifier):
    for series in payload["series"]:
        if series["provider_identifier"] == provider_identifier:
            return series

    raise ValueError("Bloomberg identifier not found")


def fetch_raw_bloomberg_history(identifier, start_date, end_date):
    raise NotImplementedError("LIVE Bloomberg access is not available")

def normalize_bloomberg_history(raw_data, canonical_ticker):
    rows = []

    for observation in raw_data:
        rows.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })

    return rows

def get_bloomberg_prices(canonical_ticker):
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]

    payload = load_bloomberg_reference_sample()
    series = find_reference_series(payload, identifier)

    return normalize_bloomberg_history(
        series["observations"],
        series["canonical_ticker"],
    )