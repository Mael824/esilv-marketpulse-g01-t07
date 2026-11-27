from pathlib import Path
import json
import csv
from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.bloomberg_provider import (fetch_raw_bloomberg_history, normalize_bloomberg_history)


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
DATA_SOURCE_LABEL="prices.csv"
YAHOO_SYMBOLS = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}
def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]

def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }



def build_market_snapshot():
    instrument_raw, instrument_ticker = fetch_raw_bloomberg_history(BLOOMBERG_IDENTIFIERS["AAPL"],"2026-09-01",
    "2026-09-30"
    )

    benchmark_raw, benchmark_ticker = fetch_raw_bloomberg_history(
    BLOOMBERG_IDENTIFIERS["SP500"],
    "2026-09-01",
    "2026-09-30"
    )

    instrument_prices = normalize_bloomberg_history(
    instrument_raw, instrument_ticker
    )

    benchmark_prices = normalize_bloomberg_history(
    benchmark_raw, benchmark_ticker
    )
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(
        aligned_instrument
    )

    benchmark_return = calculate_period_return(
        aligned_benchmark
    )

    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base_100 = calculate_base_100(
        aligned_instrument
    )

    benchmark_base_100 = calculate_base_100(
        aligned_benchmark
    )

    instrument_latest = aligned_instrument[-1]
    benchmark_latest = aligned_benchmark[-1]
    return {
    "provider": "Bloomberg stage",
    "access_mode": "APPROVED_SAMPLE",
    "lookback": LOOKBACK_LABEL,
    "interval": INTERVAL_LABEL,
    "instrument": instrument,
    "benchmark": benchmark,
    "instrument_return": instrument_return,
    "benchmark_return": benchmark_return,
    "relative_performance": relative_performance,
    "instrument_base_100": instrument_base_100,
    "benchmark_base_100": benchmark_base_100,
    "instrument_latest": instrument_latest,
    "benchmark_latest": benchmark_latest,
    "aligned_instrument": aligned_instrument,
    "aligned_benchmark": aligned_benchmark,
    }

def main():
    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]

    print("Provider")
    print(snapshot["provider"])
    print()

    print("Access mode")
    print(snapshot["access_mode"])
    print()

    print("Market configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['name']}")
    print(f"Period     : {snapshot['lookback']}")
    print(f"Interval   : {snapshot['interval']}")
    print()

    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Last price: {snapshot['instrument_latest']['close']:.2f} {instrument['currency']}")
    print(f"Period return: {snapshot['instrument_return']:.2f}%")
    print()

    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Last level: {snapshot['benchmark_latest']['close']:.2f}")
    print(f"Period return: {snapshot['benchmark_return']:.2f}%")
    print()

    print("Observations")
    print(f"{instrument['ticker']}: {len(snapshot['aligned_instrument'])}")
    print(f"{benchmark['ticker']}: {len(snapshot['aligned_benchmark'])}")
    print()

    print("Relative performance")
    print(f"{instrument['ticker']} vs {benchmark['ticker']}: {snapshot['relative_performance']:+.2f} percentage points")
    print()

    print("Base 100")
    print(f"{instrument['ticker']}: {snapshot['instrument_base_100'][0]['value']:.2f} -> {snapshot['instrument_base_100'][-1]['value']:.2f}")
    print(f"{benchmark['ticker']}: {snapshot['benchmark_base_100'][0]['value']:.2f} -> {snapshot['benchmark_base_100'][-1]['value']:.2f}")
if __name__ == "__main__":
    main()
