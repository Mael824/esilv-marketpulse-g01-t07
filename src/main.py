from pathlib import Path
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)

from providers.bloomberg_provider import (
    ACCESS_MODE,
    fetch_bloomberg_prices,
)


DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
DATA_SOURCE_LABEL = "Bloomberg stage"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def build_market_snapshot():
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = fetch_bloomberg_prices(instrument["ticker"])
    benchmark_prices = fetch_bloomberg_prices(benchmark["ticker"])

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    return {
        "provider": DATA_SOURCE_LABEL,
        "access_mode": ACCESS_MODE,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(
            instrument_return,
            benchmark_return,
        ),
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
        "instrument_last_close": aligned_instrument[-1]["close"],
        "benchmark_last_close": aligned_benchmark[-1]["close"],
        "observations": len(aligned_instrument),
    }


def main():
    snapshot = build_market_snapshot()

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
    print(f"Last price: {snapshot['instrument_last_close']:.2f} {instrument['currency']}")
    print(f"Period return: {snapshot['instrument_return']:.2f}%")
    print()

    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Market: {benchmark['market']}")
    print(f"Last level: {snapshot['benchmark_last_close']:.2f}")
    print(f"Period return: {snapshot['benchmark_return']:.2f}%")
    print()

    print("Observations")
    print(f"{instrument['ticker']}: {snapshot['observations']}")
    print(f"{benchmark['ticker']}: {snapshot['observations']}")
    print()

    print("Relative performance")
    print(f"{instrument['ticker']} vs {benchmark['ticker']} : {snapshot['relative_performance']:+.2f} percentage points")
    print()

    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    print("Base 100")
    print(f"{instrument['ticker']} : {instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}")
    print(f"{benchmark['ticker']} : {benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}")


if __name__ == "__main__":
    main()