from pathlib import Path
from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.yahoo_provider import fetch_yahoo_prices
import csv
import json
from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)

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



def main():
    instruments = load_instruments()
    prices = load_prices()
    normalized_prices = [
    normalize_price_row(row)
    for row in prices]

    normalized_prices = [
        normalize_price_row(row)
        for row in prices
    ]

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]
    instrument_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS["AAPL"],
        canonical_ticker="AAPL",
        period="1mo",
        interval="1d",
    )

    benchmark_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS["SP500"],
        canonical_ticker="SP500",
        period="1mo",
        interval="1d",
    )
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

    print("Provider")
    print("Yahoo Finance via yfinance")
    print()
    print(f"Market configuration")
    print(f"Instrument: {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark: {benchmark['ticker']} - {benchmark['name']}")
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()

    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print()

    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Market: {instrument['market']}")
    print(f"Last price: {instrument_latest['close']:.2f} {instrument['currency']}")
    print(f"Period return : {instrument_return:.2f}%")
    print()

    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Market: {benchmark['market']}")
    print(f"Last level: {benchmark_latest['close']:.2f}")
    print(f"Period return : {benchmark_return:.2f}%")
    print()

    print("Observations")
    print(f"{instrument['ticker']}: {len(aligned_instrument)}")
    print(f"{benchmark['ticker']}: {len(aligned_benchmark)}")
    print()

    print("Relative performance")
    print(f"{instrument['ticker']} vs {benchmark['ticker']} : {relative_performance:+.2f} percentage points")
    print()

    print("Base 100")
    print(f"{instrument['ticker']} : {instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}")
    print(f"{benchmark['ticker']} : {benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}")


    print("Base 100")
    print(f"{instrument['ticker']}  : {instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}")
    print(f"{benchmark['ticker']} : {benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}")

if __name__ == "__main__":
    main()
