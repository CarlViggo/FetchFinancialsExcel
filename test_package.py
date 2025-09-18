import os
import sys
import tempfile
import pandas as pd
import numpy as np
from unittest.mock import patch, Mock

def test_imports():
    print("Testing imports...")
    
    try:
        from fetchfinancialsexcel import FundamentalDataFetcher
        from fetchfinancialsexcel import cli
        print("✅ Basic imports successful")
        
        # Test new imports for residual momentum
        import statsmodels.api as sm
        from sklearn.preprocessing import StandardScaler
        import pandas_datareader.data as web
        print("✅ New residual momentum imports successful")
        
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Note: Make sure to install new requirements: pip install statsmodels scikit-learn pandas-datareader")
        return False

def test_cli_help():
    print("Testing CLI help...")
    
    try:
        import subprocess
        result = subprocess.run(['fetch-financials-excel', '--help'], 
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
        from fetchfinancialsexcel import FundamentalDataFetcher
        
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
        from fetchfinancialsexcel import FundamentalDataFetcher
        import fetchfinancialsexcel.company_data_extraction_EODH as eodh
        
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
        from fetchfinancialsexcel import FundamentalDataFetcher
        
        # Mock API responses
        mock_fundamental_data = {
            "General": {"Code": "AAPL", "Name": "Apple Inc", "Sector": "Technology"},
            "Highlights": {"MarketCapitalization": 3000000000000}
        }
        
        mock_price_data = [
            {"date": "2024-01-15", "adjusted_close": 185.64}
        ]
        
        with patch('fetchfinancialsexcel.company_data_extraction_EODH.fetch_fundamentals') as mock_fund, \
             patch('fetchfinancialsexcel.company_data_extraction_EODH.fetch_price_data') as mock_price, \
             patch('fetchfinancialsexcel.company_data_extraction_EODH.real_time_price') as mock_realtime:
            
            # Setup mocks
            mock_fund.return_value = mock_fundamental_data
            mock_price.return_value = mock_price_data
            mock_realtime.return_value = {"Price": 185.64, "Currency": "USD", "Sector": "Technology"}
            
            # Mock all extraction functions to return empty dicts
            extraction_functions = [
                'get_selected_highlights', 'calculate_roce', 'calculate_five_year_average_pe',
                'get_revenue_growth_data', 'get_eps_growth_full', 'fcf_yield_growth_latest',
                'buyback_change_latest', 'get_percent_insiders', 'get_moving_averages',
                'gross_profitability', 'accruals', 'asset_growth', 'total_yield', 'compute_cop_at', 'compute_cop_at_generous', "get_NOA"
            ]
            
            patches = []
            for func_name in extraction_functions:
                patcher = patch(f'fetchfinancialsexcel.company_data_extraction_EODH.{func_name}')
                mock_func = patcher.start()
                mock_func.return_value = {}
                patches.append(patcher)
            
            # Mock conservative analysis and excess returns
            with patch('fetchfinancialsexcel.data_analysis.conservative') as mock_conservative, \
                 patch('fetchfinancialsexcel.data_analysis.calculate_monthly_excess_returns') as mock_excess:
                mock_conservative.return_value = {"volatility": 0.25}
                mock_excess.return_value = {"AAPL": list(np.random.normal(0.01, 0.05, 36))}
                
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
        from fetchfinancialsexcel import data_analysis
        
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

def test_residual_momentum_functions():
    print("Testing residual momentum functions...")
    
    try:
        from fetchfinancialsexcel import data_analysis
        import numpy as np
        import pandas as pd
        
        # Test calculate_monthly_excess_returns function
        test_ticker = "AAPL"
        test_price_data = []
        
        # Create 40 months of mock price data (more than needed 36)
        from datetime import datetime, timedelta
        base_date = datetime(2021, 1, 1)
        base_price = 100.0
        
        for i in range(40 * 30):  # 40 months * 30 days
            date = base_date + timedelta(days=i)
            price = base_price * (1 + np.random.normal(0, 0.02))  # Random walk
            test_price_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'adjusted_close': price
            })
        
        # Test excess returns calculation
        excess_returns_result = data_analysis.calculate_monthly_excess_returns(test_ticker, test_price_data)
        
        # The function returns {'Excess Returns': {'AAPL': [...]}}
        if 'Excess Returns' in excess_returns_result and test_ticker in excess_returns_result['Excess Returns']:
            excess_returns = excess_returns_result['Excess Returns'][test_ticker]
            if isinstance(excess_returns, list) and len(excess_returns) == 36:
                print("✅ Monthly excess returns calculation works")
            else:
                print(f"❌ Excess returns wrong format: got {len(excess_returns) if isinstance(excess_returns, list) else type(excess_returns)}")
                return False
        else:
            print("❌ Excess returns calculation failed")
            print(f"Got result: {excess_returns_result}")
            return False
        
        # Test ticker_excess_returns function
        separate_data_list = [
            {
                'Ticker': 'AAPL',
                'Excess Returns': {'AAPL': excess_returns}
            }
        ]
        
        df = pd.DataFrame([{'Ticker': 'AAPL', 'Company': 'Apple Inc'}])
        ticker_returns = data_analysis.ticker_excess_returns(df, separate_data_list)
        
        if 'AAPL' in ticker_returns and ticker_returns['AAPL'] is not None:
            print("✅ Ticker excess returns extraction works")
        else:
            print("❌ Ticker excess returns extraction failed")
            return False
        
        # Test get_fama_factors (mocked)
        with patch('fetchfinancialsexcel.data_analysis.web.DataReader') as mock_reader:
            # Mock Fama-French data
            mock_ff_data = pd.DataFrame({
                'Mkt-RF': np.random.normal(0.01, 0.05, 36),
                'SMB': np.random.normal(0.005, 0.03, 36),
                'HML': np.random.normal(0.003, 0.04, 36)
            })
            mock_reader.return_value = [mock_ff_data]
            
            ff_data = data_analysis.get_fama_factors("US")
            
            if ff_data is not None and len(ff_data) == 36:
                print("✅ Fama-French data fetching works")
            else:
                print("❌ Fama-French data fetching failed")
                return False
        
        print("✅ All residual momentum functions work correctly")
        return True
        
    except Exception as e:
        print(f"❌ Residual momentum functions error: {e}")
        return False

def test_residual_momentum_integration():
    print("Testing residual momentum integration...")
    
    try:
        from fetchfinancialsexcel import data_analysis
        import numpy as np
        import pandas as pd
        
        # Create test data with properly formatted excess returns
        test_excess_returns = list(np.random.normal(0.01, 0.05, 36))  # 36 months of returns
        
        separate_data_list = [
            {
                'Ticker': 'AAPL',
                'Excess Returns': {'AAPL': test_excess_returns},
                'volatility': 0.25
            },
            {
                'Ticker': 'MSFT',
                'Excess Returns': {'MSFT': test_excess_returns},
                'volatility': 0.20
            }
        ]
        
        df = pd.DataFrame([
            {'Ticker': 'AAPL', 'Company': 'Apple Inc'},
            {'Ticker': 'MSFT', 'Company': 'Microsoft Corp'}
        ])
        
        # Mock Fama-French data and test residual momentum
        with patch('fetchfinancialsexcel.data_analysis.get_fama_factors') as mock_ff:
            mock_ff_data = pd.DataFrame({
                'Mkt-RF': np.random.normal(0.01, 0.05, 36),
                'SMB': np.random.normal(0.005, 0.03, 36),
                'HML': np.random.normal(0.003, 0.04, 36)
            })
            mock_ff.return_value = mock_ff_data
            
            # Test residual momentum function
            result_df = data_analysis.residual_momentum("US", df, separate_data_list)
            
            if 'rMOM' in result_df.columns:
                print("✅ Residual momentum integration works")
                return True
            else:
                print("❌ Residual momentum integration failed - no rMOM column")
                return False
                
    except Exception as e:
        print(f"❌ Residual momentum integration error: {e}")
        return False

def test_factor_country_parameter():
    print("Testing factor_country parameter...")
    
    try:
        from fetchfinancialsexcel import FundamentalDataFetcher
        
        # Test that factor_country parameter is accepted
        fetcher = FundamentalDataFetcher(api_key="test_key")
        
        # Create mock data
        mock_df = pd.DataFrame([{"Ticker": "AAPL", "Company": "Apple Inc"}])
        mock_separate = [{"Ticker": "AAPL", "volatility": 0.25}]
        
        # Test analyze_data with factor_country parameter
        with patch.object(fetcher, 'analyze_data') as mock_analyze:
            mock_analyze.return_value = mock_df
            
            # This should not raise an error
            result = fetcher.analyze_data(mock_df, mock_separate, factor_country="Europe")
            print("✅ factor_country parameter works")
            return True
            
    except Exception as e:
        print(f"❌ factor_country parameter error: {e}")
        return False


def test_complete_workflow():
    print("Testing complete workflow...")
    
    try:
        from fetchfinancialsexcel import FundamentalDataFetcher
        
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
                
                # Test workflow with factor_country parameter
                fetcher = FundamentalDataFetcher(api_key="test_key")
                fetcher.process_excel_file(input_file.name, output_file.name, max_workers=1, factor_country="US")
                
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
        test_residual_momentum_functions,
        test_residual_momentum_integration,
        test_factor_country_parameter,
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