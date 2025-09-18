# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-01-18

### Added
- **Residual Momentum Analysis**: New comprehensive residual momentum (rMOM) calculation using Fama-French 3-factor model
- **Monthly Excess Returns**: New `calculate_monthly_excess_returns` function calculating 36 months of risk-adjusted returns
- **Fama-French Integration**: Automatic fetching of Fama-French factors for US and European markets via `pandas-datareader`
- **Factor Country Support**: New `factor_country` parameter in `process_excel_file()` to specify market region ("US" or "Europe")
- **Advanced Regression Analysis**: OLS regression with standardized residuals for momentum calculation
- **Robust Error Handling**: Comprehensive safety checks for network failures, data validation, and graceful degradation

### New Dependencies
- **statsmodels>=0.13.0**: For OLS regression analysis
- **scikit-learn>=1.0.0**: For data standardization (StandardScaler)
- **pandas-datareader>=0.10.0**: For Fama-French factor data retrieval

### Improved
- **API Compatibility**: Enhanced `analyze_data()` method with `factor_country` parameter while maintaining backward compatibility
- **Data Pipeline**: Extended data flow to include price data in analysis pipeline for momentum calculations
- **Safety Features**: All residual momentum functions include NaN/infinity checks, data length validation, and network error handling
- **Test Coverage**: Extended test suite with 10/10 tests passing, including comprehensive residual momentum testing

### Technical Details
- **Risk-Free Rate**: Configurable risk-free rate (default 1.02 for 2% annual)
- **Momentum Window**: Uses months t-6 to t-2 for momentum calculation to avoid reversal effects
- **Data Requirements**: Requires minimum 36 months of price data for residual momentum calculation
- **Fallback Behavior**: Returns original DataFrame with None values if residual momentum calculation fails

## [0.2.0] - 2025-01-28

### Added
- **Revised COP/AT Calculation**: New `compute_cop_at_generous` function providing an alternative COP/AT calculation method
- **Enhanced Data Output**: Excel files now include both `cop_at` (original) and `cop_at_revised` (new generous calculation)
- **Comprehensive Data Cleaning**: Advanced Excel export cleaning to prevent XML corruption errors
- **Multiple Excel Engines**: Automatic fallback between openpyxl and xlsxwriter for robust Excel file generation
- **Debug Information**: Added diagnostic output to identify problematic data before Excel export

### Improved
- **Excel Compatibility**: Enhanced data validation and cleaning prevents Excel XML errors
- **Column Names**: Cleaned column naming (removed spaces, special characters) for better Excel compatibility
- **Error Handling**: Graceful fallbacks for Excel writing issues with CSV export as last resort
- **NumPy Compatibility**: Fixed compatibility issues with NumPy 1.x/2.x versions

### Fixed
- **Data Type Issues**: Proper handling of infinite values, NaN, and complex data types in Excel export
- **Import Errors**: Resolved module import order issues causing UnboundLocalError

## [0.1.1] - 2025-01-28

### Fixed
- **NOA Function**: Fixed critical bug in `get_NOA` function where extra comma created tuple instead of numeric value, causing "type tuple doesn't define __round__ method" error
- **NOA Return Format**: Standardized NOA function to consistently return `{"NOA_GR1A": value}` instead of inconsistent key names
- **Data Validation**: Added robust error handling in NOA helper functions to prevent crashes when insufficient historical data is available
- **Import Issues**: Resolved urllib3 dependency conflicts that caused package import failures

### Improved
- **Error Handling**: Enhanced all NOA helper functions with proper data validation
- **Code Quality**: Removed unnecessary f-strings and improved code consistency
- **Test Coverage**: All 7/7 tests now pass including NOA functionality

## [0.1.0] - 2025-01-24

### Added
- Initial release of FetchFinancialsExcel package
- Fundamental data fetching from EODHD API
- Excel file processing for batch company analysis
- Financial metrics calculation including ROCE, P/E ratios, revenue growth
- Data analysis functions including Greenblatt formula
- CLI interface for command-line usage
- NOA (Net Operating Assets) calculation functionality

