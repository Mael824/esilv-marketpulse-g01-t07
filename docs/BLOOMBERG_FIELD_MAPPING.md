# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

Source:
data/sample/bloomberg_reference_sample.json

Reference:
docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md

Live connectivity:
not demonstrated

Note:
The instructor reference is unavailable.
Instructor approval is pending.

## Instrument input

- Provider identifier: AAPL US Equity
- Canonical ticker: AAPL
- Date format: YYYY-MM-DD
- Data structure: JSON series with a list of observations.

Available fields:
- observation_date
- open_value
- high_value
- low_value
- close_value
- volume_value

These are teaching wrapper keys, not Bloomberg field mnemonics.

## Benchmark input

- Provider identifier: SPX Index
- Canonical ticker: SP500
- Date format: YYYY-MM-DD
- Data structure: JSON with a list of observations.

Available fields:
- observation_date
- open_value
- high_value
- low_value
- close_value
- volume_value

The first observation has a volume of 0.

The fields are the same as for AAPL. They are teaching wrapper keys, not Bloomberg field mnemonics.

SPX Index is the Bloomberg identifier, but MarketPulse still uses SP500.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | observation_date | YYYY-MM-DD |
| ticker | application mapping | AAPL or SP500 |
| open | open_value | Opening price |
| high | high_value | Highest price |
| low | low_value | Lowest price |
| close | close_value | Closing price |
| volume | volume_value | Volume |

The source fields are teaching wrapper keys, not Bloomberg LIVE field mnemonics.

The mapping is based on the sample JSON file because the instructor reference is unavailable.

## Preserve canonical tickers

MarketPulse uses AAPL and SP500, even if the Bloomberg identifiers are different.

Example for SP500:

```python
{
    "date": "2026-09-01",
    "ticker": "SP500",
    "open": 6592,
    "high": 6615,
    "low": 6580,
    "close": 6600,
    "volume": 0
}
```

For now, we only document the expected format.
The normalization will be done in TD10.

## TD10 handoff

- Access mode: APPROVED_SAMPLE (approval pending)
- Instrument identifier: AAPL US Equity
- Benchmark identifier: SPX Index
- Date representation: YYYY-MM-DD
- Input structure: JSON with a list of observations for each series.
- Missing fields: None found.
- Special normalization notes: Keep AAPL and SP500 as canonical tickers. Map the teaching wrapper keys to MarketPulse fields and keep zero volume values.

Expected canonical reference:
data/sample/bloomberg_reference_expected.json