# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

Source: data/sample/bloomberg_reference_sample.json
Reference: docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md
Live connectivity: not demonstrated

The sample is an instructor-approved fallback fixture (`is_live_bloomberg_output: false`). Its values are illustrative teaching values reused from `data/sample/prices.csv`, not certified Bloomberg observations. This document does not prove live Bloomberg connectivity.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

The provider identifier is not the canonical ticker. MarketPulse and `analytics.py` keep receiving `AAPL` and `SP500`.

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | Teaching wrapper key. ISO string `YYYY-MM-DD` |
| ticker | application mapping | `canonical_ticker` of the series: AAPL or SP500, never the provider identifier |
| open | `open_value` | Teaching wrapper key. Numeric |
| high | `high_value` | Teaching wrapper key. Numeric |
| low | `low_value` | Teaching wrapper key. Numeric |
| close | `close_value` | Teaching wrapper key. Numeric |
| volume | `volume_value` | Teaching wrapper key. Numeric; `0` for SPX Index in this sample |

Teaching wrapper key != Bloomberg LIVE field mnemonic. These keys come from the fallback fixture and are not Bloomberg field names.

The mapping was checked against `data/sample/bloomberg_reference_expected.json`: the expected canonical rows contain the same values as the corresponding sample observations.

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity (canonical ticker AAPL)
- Benchmark identifier: SPX Index (canonical ticker SP500)
- Date representation: `observation_date` as a `YYYY-MM-DD` string (21 observations per series, 2026-09-01 to 2026-09-30)
- Input structure: top-level `series` list; each series has `role`, `canonical_ticker`, `provider_identifier` and an `observations` list of objects with the six wrapper keys
- Missing fields: none in the sample; the benchmark volume is `0` (no real volume for an index in this fixture)
- Special normalization notes: take `ticker` from `canonical_ticker`, not from `provider_identifier`; values are already numeric, so no text-to-number conversion is needed, but cast to `float` for prices and `int` for volume to match the canonical row types
- Expected canonical reference: data/sample/bloomberg_reference_expected.json