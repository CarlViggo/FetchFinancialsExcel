import os
import sys
import tempfile
import pandas as pd
from unittest.mock import patch, Mock

def test_imports():
    print("Testing imports...")
    
    try:
        from fetch_fundamental_data import FundamentalDataFetcher
        from fetch_fundamental_data import cli
        print("All imports successful")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False

def test_cli_help():
    print("Testing CLI help...")
    
    try:
        import subprocess
        result = subprocess.run(['fetch-fundamentals', '--help'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and 'EODHD API key' in result.stdout:
            print("CLI help works correctly")
            return True
        else:
            print(f"CLI help failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"CLI test error: {e}")
        return False

def test_excel_processing():
    print("Testing Excel processing...")
    
    try:
        from fetch_fundamental_data import FundamentalDataFetcher
        
        # Create test Excel file
        test_data = [
            ['Company Name', 'Ticker'],
            ['Apple Inc', 'AAPL'],
            ['Microsoft Corporation', 'MSFT'],
            ['Tesla Inc', 'TSLA']
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            df = pd.DataFrame(test_data)
            df.to_excel(tmp.name, index=False, header=False)
            
            # Test ticker extraction
            fetcher = FundamentalDataFetcher(api_key="test_key")
            companies, tickers = fetcher.extract_tickers_from_excel(tmp.name)
            
            expected_companies = ['APPLE INC', 'MICROSOFT CORPORATION', 'TESLA INC']
            expected_tickers = ['AAPL', 'MSFT', 'TSLA']
            
            if companies == expected_companies and tickers == expected_tickers:
                print("Excel processing works correctly")
                result = True
            else:
                print(f"Excel processing failed. Got: {companies}, {tickers}")
                result = False
        
        os.unlink(tmp.name)
        return result
        
    except Exception as e:
        print(f"Excel processing error: {e}")
        return False

def test_api_key_handling():
    print("Testing API key handling...")
    
    try:
        from fetch_fundamental_data import FundamentalDataFetcher
        import fetch_fundamental_data.company_data_extraction_EODH as eodh
        
        # Test setting API key
        test_key = "test_api_key_123"
        fetcher = FundamentalDataFetcher(api_key=test_key)
        
        if fetcher.api_key == test_key and eodh.API_KEY == test_key:
            print("API key handling works correctly")
            return True
        else:
            print("API key not set correctly")
            return False
            
    except Exception as e:
        print(f"API key handling error: {e}")
        return False

def test_data_fetching_mock():
    print("Testing data fetching (mocked)...")
    
    try:
        from fetch_fundamental_data import FundamentalDataFetcher
        
        # Mock API responses
        mock_fundamental_data = {
            "General": {"Code": "AAPL", "Name": "Apple Inc", "Sector": "Technology"},
            "Highlights": {"MarketCapitalization": 3000000000000}
        }
        
        mock_price_data = [
            {"date": "2024-01-15", "adjusted_close": 185.64}
        ]
        
        with patch('fetch_fundamental_data.company_data_extraction_EODH.fetch_fundamentals') as mock_fund, \
             patch('fetch_fundamental_data.company_data_extraction_EODH.fetch_price_data') as mock_price, \
             patch('fetch_fundamental_data.company_data_extraction_EODH.real_time_price') as mock_realtime:
            
            # Setup mocks
            mock_fund.return_value = mock_fundamental_data
            mock_price.return_value = mock_price_data
            mock_realtime.return_value = {"Price": 185.64, "Currency": "USD", "Sector": "Technology"}
            
            # Mock all extraction functions to return empty dicts
            extraction_functions = [
                'get_selected_highlights', 'calculate_roce', 'calculate_five_year_average_pe',
                'get_revenue_growth_data', 'get_eps_growth_full', 'fcf_yield_growth_latest',
                'buyback_change_latest', 'get_percent_insiders', 'get_moving_averages',
                'gross_profitability', 'accruals', 'asset_growth', 'total_yield', 'compute_cop_at'
            ]
            
            patches = []
            for func_name in extraction_functions:
                patcher = patch(f'fetch_fundamental_data.company_data_extraction_EODH.{func_name}')
                mock_func = patcher.start()
                mock_func.return_value = {}
                patches.append(patcher)
            
            # Mock conservative analysis
            with patch('fetch_fundamental_data.data_analysis.conservative') as mock_conservative:
                mock_conservative.return_value = {"volatility": 0.25}
                
                # Test fetching
                fetcher = FundamentalDataFetcher(api_key="test_key")
                combined, other = fetcher.fetch_company_data("AAPL")
                
                if isinstance(combined, dict) and isinstance(other, dict):
                    print("Data fetching works correctly")
                    result = True
                else:
                    print("Data fetching failed")
                    result = False
            
            # Cleanup patches
            for patcher in patches:
                patcher.stop()
                
            return result
            
    except Exception as e:
        print(f"Data fetching error: {e}")
        return False

def test_analysis_functions():
    print("Testing analysis functions...")
    
    try:
        from fetch_fundamental_data import data_analysis
        
        # Create test dataframe - using current year for PE column
        from datetime import datetime
        current_year = datetime.now().year
        
        test_df = pd.DataFrame([
            {"Ticker": "AAPL", "Bolag": "Apple Inc", f"PE {current_year}": 25.5, "ROCE": 0.25, "ROE": 0.30}
        ])
        
        # Test Greenblatt formula
        result_df = data_analysis.greenblatt_formula(test_df.copy())
        
        if "Greenblatt Formula" in result_df.columns:
            print("Analysis functions work correctly")
            return True
        else:
            print("Analysis functions failed")
            return False
            
    except Exception as e:
        print(f"Analysis functions error: {e}")
        return False


def test_complete_workflow():
    print("Testing complete workflow...")
    
    try:
        from fetch_fundamental_data import FundamentalDataFetcher
        
        # Create test Excel file
        test_data = [
            ['Company Name', 'Ticker'],
            ['Apple Inc', 'AAPL']
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as input_file, \
             tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as output_file:
            
            # Create input file
            df = pd.DataFrame(test_data)
            df.to_excel(input_file.name, index=False, header=False)
            
            # Mock the entire data fetching process
            with patch.object(FundamentalDataFetcher, 'fetch_all_data') as mock_fetch, \
                 patch.object(FundamentalDataFetcher, 'analyze_data') as mock_analyze:
                
                # Setup mocks
                mock_df = pd.DataFrame([{"Ticker": "AAPL", "Bolag": "Apple Inc", "Price": 185.64}])
                mock_separate = [{"Ticker": "AAPL", "volatility": 0.25}]
                mock_fetch.return_value = (mock_df, mock_separate)
                mock_analyze.return_value = mock_df
                
                # Test workflow
                fetcher = FundamentalDataFetcher(api_key="test_key")
                fetcher.process_excel_file(input_file.name, output_file.name, max_workers=1)
                
                # Check if output file was created
                if os.path.exists(output_file.name):
                    result_df = pd.read_excel(output_file.name)
                    if len(result_df) > 0 and 'Ticker' in result_df.columns:
                        print("Complete workflow works correctly")
                        result = True
                    else:
                        print("Output file has incorrect format")
                        result = False
                else:
                    print("Output file not created")
                    result = False
        
        # Cleanup
        for filepath in [input_file.name, output_file.name]:
            if os.path.exists(filepath):
                os.unlink(filepath)
                
        return result
        
    except Exception as e:
        print(f"Complete workflow error: {e}")
        return False

def run_all_tests():
    print("Running fetch-fundamental-data package tests")
    print("===========================================")
    
    tests = [
        test_imports,
        test_api_key_handling,
        test_excel_processing,
        test_data_fetching_mock,
        test_analysis_functions,
        test_complete_workflow,
        test_cli_help
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f" Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! Package is ready for use.")
        return True
    else:
        print(" Some tests failed. Please review before pushing.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 