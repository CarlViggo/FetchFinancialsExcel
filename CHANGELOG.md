# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

