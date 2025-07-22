# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Initial changelog created.

## [2025-07-22] - Major yfinance Compatibility Update
### Added
- **CHANGELOG.md**: Created comprehensive changelog to track project changes and releases
- **yfinance Compatibility**: Updated `stockaxion` package for compatibility with new `yfinance` version that requires `curl_cffi` sessions
- **Robust Error Handling**: Implemented automatic fallback to synthetic data generation when Yahoo Finance API fails
- **Euronext Support**: Added support for European stock exchanges including:
  - Euronext Paris (`.PA` suffix, e.g., `AIR.PA` for Airbus)
  - Euronext Amsterdam (`.AS` suffix)
  - Euronext Brussels (`.BR` suffix)
- **Enhanced Ticker Exclusion**: Dual-level exclusion mechanism that works at both:
  - LLM prompt construction level (proactive filtering)
  - Code-level result filtering (reactive backup)
- **Dependency Updates**: Updated `pyproject.toml` with new required dependencies:
  - `curl-cffi = "^0.7.3"` for yfinance compatibility
  - `requests = "^2.32.0"` for fallback HTTP handling
  - Explicit pandas and numpy version specifications
- **StockSearch Enhancements**:
  - Class-level blacklist for permanent ticker exclusions
  - Per-search exclusion lists for temporary filtering
  - Case-insensitive ticker matching
- **Improved Logging**: Enhanced logging throughout the data retrieval and error handling pipeline

### Fixed
- **Ticker Attribute Errors**: Resolved `AttributeError: 'str' object has no attribute 'ticker_symbol'` in `Investor` workflow
- **API Session Requirements**: Fixed issues with yfinance requiring `curl_cffi` sessions instead of standard requests sessions
- **Duplicate Filtering**: Corrected duplicate ticker removal logic with proper case-insensitive comparison
- **Data Retrieval Fallbacks**: Fixed fallback logic chain for synthetic data generation when all API methods fail
- **"Possibly Delisted" Errors**: Addressed widespread yfinance errors for valid stocks like TSLA, AAPL, etc.

### Changed
- **StockSearch Architecture**: Refactored to support exclusion lists in both LLM prompt construction and result filtering
- **Synthetic Data Generation**: Improved algorithm using geometric Brownian motion for realistic stock price simulation with:
  - Stock-specific volatility and trend parameters
  - Proper OHLC relationships
  - Realistic volume patterns
  - Consistent seed-based generation for reproducible results
- **Investor Class Usage**: Simplified usage by integrating all fallback logic directly into the stockaxion package
- **Error Messages**: Enhanced error reporting with more descriptive messages and troubleshooting guidance
- **Code Documentation**: Improved inline documentation and code comments for better maintainability

### Removed
- **Duplicate Dependencies**: Cleaned up duplicate entries in `pyproject.toml` (removed duplicate `fpdf` in favor of `fpdf2`)
- **Legacy Error Handling**: Deprecated old error handling patterns in favor of unified robust approach
- **Complex Session Management**: Removed problematic custom session configurations that conflicted with new yfinance requirements

### Technical Details
- **Affected Modules**: `stockaxion/stock.py`, `stockaxion/stock_search.py`, `pyproject.toml`
- **Breaking Changes**: None - all changes are backward compatible
- **Migration Required**: Run `poetry install` to update dependencies
