# Fetch Fundamental Data

A Python package for fetching and analyzing fundamental financial data using the EODHD API. This package allows you to process Excel files containing stock tickers and generate financial analysis reports.

## Features

- **Concurrent Data Fetching**: Efficiently fetches financial data for multiple stocks simultaneously
- **Comprehensive Analysis**: Calculate key financial metrics not avaibale in EODHD including:
  - Greenblatt Magic Formula rankings
  - Conservative investment scores
  - Quality scores
  - P/E ratios, ROCE, revenue growth, EPS growth
  - Free cash flow metrics, buyback data, insider ownership
  - Technical indicators and moving averages
- **Excel Integration**: Read ticker lists from Excel and output results to Excel
- **Professional CLI**: Easy-to-use command-line interface
- **Robust Error Handling**: Graceful handling of API failures and missing data

## Installation

### From PyPI (when published)
```bash
pip install fetch-fundamental-data
```

### From Source
```bash
git clone https://github.com/username/fetch-fundamental-data.git
cd fetch-fundamental-data
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/username/fetch-fundamental-data.git
cd fetch-fundamental-data
pip install -r requirements.txt
pip install -e .
```

## Prerequisites

1. **EODHD API Key**: You need an API key from [EODHD](https://eodhd.com/) to fetch financial data
2. **Python 3.8+**: This package requires Python 3.8 or higher

## Quick Start

### 1. Prepare Excel File

Create an Excel file (`.xlsx` or `.xls`) with the following format:

| Company Name | Ticker |
|--------------|--------|
| Apple Inc    | AAPL   |
| Google       | GOOGL  |
| Microsoft    | MSFT   |
| Danske Bank  | DANSKE.CO |

**Important Notes:**
- First row can be headers (will be skipped)
- Column A: Company names
- Column B: Ticker symbols
- Use proper ticker formats (e.g., `DANSKE.CO` for Copenhagen exchange)

### 2. Run the Analysis

```bash
fetch-fundamentals --api-key YOUR_EODHD_API_KEY --input tickers.xlsx --output results.xlsx
```

### 3. View Results

The output Excel file will contain comprehensive financial data and analysis for all tickers.

## Command Line Usage

### Basic Usage
```bash
fetch-fundamentals --api-key YOUR_API_KEY --input input.xlsx --output output.xlsx
```

### Advanced Usage
```bash
# Custom number of concurrent workers (default: 10)
fetch-fundamentals --api-key YOUR_API_KEY --input tickers.xlsx --output results.xlsx --workers 5

# Short form arguments
fetch-fundamentals --api-key YOUR_API_KEY -i tickers.xlsx -o results.xlsx -w 5
```

### Command Line Arguments

| Argument | Short | Required | Description |
|----------|-------|----------|-------------|
| `--api-key` | | Yes | Your EODHD API key |
| `--input` | `-i` | Yes | Path to input Excel file |
| `--output` | `-o` | YEs | Path to output Excel file |
| `--workers` | `-w` | | Number of concurrent workers (1-50, default: 10) |
| `--version` | | | Show version information |
| `--help` | `-h` | | Show help message |

## Python API Usage

You can also use the package programmatically:

```python
from fetch_fundamental_data import FundamentalDataFetcher

# Initialize with your API key
fetcher = FundamentalDataFetcher(api_key="YOUR_EODHD_API_KEY")

# Process an Excel file
fetcher.process_excel_file(
    input_file="path/to/tickers.xlsx",
    output_file="path/to/results.xlsx",
    max_workers=10
)

# Or work with data directly
company_list, ticker_list = fetcher.extract_tickers_from_excel("tickers.xlsx")
df, separate_data = fetcher.fetch_all_data(company_list, ticker_list)
analyzed_df = fetcher.analyze_data(df, separate_data)
```

## Output Data

The output Excel file contains the following types of data:

### Financial Metrics
- **Price Information**: Current price, currency, sector
- **Valuation Ratios**: P/E ratios (current and 5-year average), ROCE
- **Growth Metrics**: Revenue growth, EPS growth, asset growth
- **Profitability**: Gross profitability, free cash flow metrics
- **Balance Sheet**: Accruals, total yield, insider ownership percentage

### Analysis Scores
- **Greenblatt Formula**: Magic Formula ranking based on P/E and ROCE
- **Conservative Formula**: Risk-adjusted scoring based on volatility, NPY, and momentum
- **Quality Score**: Overall quality assessment

### Technical Data
- **Moving Averages**: Various period moving averages
- **Volatility Metrics**: Historical volatility measures
- **Price Momentum**: Momentum indicators

## Examples

### Example Input File (`tickers.xlsx`)

| Company | Ticker |
|---------|--------|
| Apple | AAPL |
| Microsoft | MSFT |
| Alphabet | GOOGL |
| Amazon | AMZN |
| Tesla | TSLA |

### Example Usage

```bash
# Basic analysis
fetch-fundamentals --api-key abc123xyz --input tickers.xlsx --output analysis.xlsx

# High-speed processing (more workers)
fetch-fundamentals --api-key abc123xyz --input large_portfolio.xlsx --output results.xlsx --workers 20

# Conservative processing (fewer workers, good for rate limits)
fetch-fundamentals --api-key abc123xyz --input tickers.xlsx --output results.xlsx --workers 3
```

## Testing

Before pushing changes, run the test script to validate functionality:

```bash
python test_package.py
```

This will test:
- Package imports
- CLI functionality  
- Excel file processing
- API key handling
- Data fetching (mocked)
- Analysis functions
- Complete workflow

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Carl Viggo Gravenhorst-Lövenstierne**