from pathlib import Path
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)

from providers.bloomberg_provider import get_bloomberg_prices


DATA_DIR = Path(__file__).resolve().parents[1] / "data/sample"

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
DATA_SOURCE_LABEL = "Bloomberg stage"
ACCESS_MODE = "APPROVED_SAMPLE"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def build_market_snapshot(provider_mode="APPROVED_SAMPLE"):
    if provider_mode != ACCESS_MODE:
        raise NotImplementedError("LIVE Bloomberg access is not available")

    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = get_bloomberg_prices(instrument["ticker"])
    benchmark_prices = get_bloomberg_prices(benchmark["ticker"])

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    return {
        "provider": DATA_SOURCE_LABEL,
        "access_mode": ACCESS_MODE,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
        "instrument_latest": aligned_instrument[-1],
        "benchmark_latest": aligned_benchmark[-1],
    }


def print_market_snapshot(snapshot):
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]

    print("=== MarketPulse ===")
    print()

    print("Provider")
    print(snapshot["provider"])
    print()

    print("Access mode")
    print(snapshot["access_mode"])
    print()

    print("Market configuration")
    print(f"Period: {snapshot['lookback']}")
    print(f"Interval: {snapshot['interval']}")
    print()

    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Market: {instrument['market']}")
    print(f"Last price: {snapshot['instrument_latest']['close']:.2f} {instrument['currency']}")
    print(f"Period return: {snapshot['instrument_return']:.2f}%")
    print()

    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Market: {benchmark['market']}")
    print(f"Last level: {snapshot['benchmark_latest']['close']:.2f}")
    print(f"Period return: {snapshot['benchmark_return']:.2f}%")
    print()

    print("Observations")
    print(f"AAPL: {len(snapshot['instrument_base_100'])}")
    print(f"SP500: {len(snapshot['benchmark_base_100'])}")
    print()

    print("Relative performance")
    print(f"AAPL vs SP500: {snapshot['relative_performance']:+.2f} percentage points")
    print()

    print("Base 100")
    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    print(f"AAPL: {instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}")
    print(f"SP500: {benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}")


def main():
    snapshot = build_market_snapshot()
    print_market_snapshot(snapshot)


if __name__ == "__main__":
    main()