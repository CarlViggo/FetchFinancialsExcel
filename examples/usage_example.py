import os
import pandas as pd
from fetch_fundamental_data import FundamentalDataFetcher

def create_sample_excel():
    data = [
        ['Company Name', 'Ticker'],
        ['Apple Inc', 'AAPL'],
        ['Microsoft Corporation', 'MSFT'],
        ['Alphabet Inc', 'GOOGL'],
        ['Amazon.com Inc', 'AMZN'],
        ['Tesla Inc', 'TSLA']
    ]
    
    df = pd.DataFrame(data)
    df.to_excel('sample_tickers.xlsx', index=False, header=False)
    print("Created sample_tickers.xlsx")

def example_programmatic_usage():
    print("\nExample: Programmatic Usage")
    print("=" * 50)
    
    # replace this with your API key
    api_key = "YOUR API KEY HERE"
    
    try:
        # initialize the fetcher
        fetcher = FundamentalDataFetcher(api_key=api_key)
        
        # extract tickers from Excel file
        company_list, ticker_list = fetcher.extract_tickers_from_excel("sample_tickers.xlsx")
        print(f"Found {len(ticker_list)} tickers: {ticker_list}")
        
        df, separate_data = fetcher.fetch_all_data(company_list, ticker_list, max_workers=3)
        analyzed_df = fetcher.analyze_data(df, separate_data)
        
        analyzed_df.to_excel("results.xlsx", index=False)
        
        print("Results saved to results.xlsx")
        
    except Exception as e:
        print(f"Error: {e}")

def example_cli_usage():
    print("\n  Example: Command Line Usage")
    print("=" * 50)
    
    print("Basic usage:")
    print("fetch-fundamentals --api-key YOUR_API_KEY --input sample_tickers.xlsx --output results.xlsx")
    print()
    
    print("With custom workers:")
    print("fetch-fundamentals --api-key YOUR_API_KEY -i sample_tickers.xlsx -o results.xlsx -w 5")
    print()
    
    print("Get help:")
    print("fetch-fundamentals --help")

if __name__ == "__main__":
    print("Fetch Fundamental Data - Usage Examples")
    print("=======================================")
    
    # create sample file
    create_sample_excel()
    
    # show examples
    example_cli_usage()
    example_programmatic_usage()