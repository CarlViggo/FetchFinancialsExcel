# Examples

This directory contains example files and usage demonstrations for the `FetchFinancialsExcel` package.

## Files

- **`usage_example.py`** - Complete usage example showing both CLI and programmatic usage
- **`sample_tickers.xlsx`** - Sample Excel file with stock tickers (will be created by usage_example.py)

## Quick Start

1. **Run the usage example:**
   ```bash
   cd examples
   python usage_example.py
   ```

2. **Try the CLI with the sample file:**
   ```bash
   fetch-financials-excel --api-key YOUR_EODHD_API_KEY --input examples/sample_tickers.xlsx --output results.xlsx
   ```

## Sample Excel Format

The `sample_tickers.xlsx` file demonstrates the expected format:

| Company Name | Ticker |
|--------------|--------|
| Apple Inc | AAPL |
| Microsoft Corporation | MSFT |
| Alphabet Inc | GOOGL |
| Amazon.com Inc | AMZN |
| Tesla Inc | TSLA |

## API Key

You'll need an API key from [EODHD](https://eodhd.com/) to fetch actual financial data. Replace `YOUR_EODHD_API_KEY` in the examples with your real API key.

## Expected Output

The package will generate an Excel file with comprehensive financial analysis including:

- Current stock prices and basic info
- Financial ratios (P/E, ROCE, etc.)
- Growth metrics (revenue, EPS, etc.)
- Quality scores and rankings
- Technical indicators

## Notes

- The sample file contains major US stocks that should work with most EODHD subscriptions
- Processing time depends on your API subscription and number of workers
- Results will vary based on current market data and availability 