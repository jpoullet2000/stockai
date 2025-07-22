# StockAxion 📈

**Find opportunities to invest in stocks using AI-powered pattern recognition and technical analysis.**

StockAxion is a Python library that helps investors identify potential stock opportunities by analyzing market patterns, technical indicators, and generating comprehensive PDF reports.

## Features

- 🔍 **Smart Stock Search**: AI-powered stock discovery based on search criteria
- 📊 **Pattern Recognition**: Built-in detection for technical patterns like "rise and fall", RSI signals
- 🎯 **Stock Filtering**: Filter stocks based on multiple technical indicators and patterns
- 📋 **PDF Reports**: Generate detailed investment reports with charts and analysis
- 🛠️ **Flexible API**: Easily customize analysis parameters and patterns

## Installation

This project uses Poetry for dependency management. To install:

```bash
# Clone the repository
git clone <repository-url>
cd stockai

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

## Setup

1. Create a `.env` file in the project root
2. Add your XAI API key:

```env
XAI_API_KEY=your_xai_api_key_here
```

## Quick Start

### Basic Analysis

Run a comprehensive stock analysis with default settings:

```python
from stockaxion.api import Investor

investor = Investor()
investor.run()
```

This will:
1. Search for stocks using AI
2. Apply technical pattern filters
3. Generate a PDF report with findings

### Custom Search Criteria

Specify search criteria for targeted analysis:

```python
investor = Investor(extra_params={"search_criteria": ["cup_and_handle"]})
investor.run(use_filters=False)
```

The `use_filters=False` option means no additional filters will be applied to the search results (typically returns ~10 stocks).

### Analyze Specific Stocks

Analyze predetermined stocks with custom patterns:

```python
investor = Investor(
    stocks=['TSLA', 'RIVN', 'PLTR', 'ROKU'],
    patterns=["check_rise_then_fall"],
    extra_params={
        "search_criteria": ["rise_and_fall"], 
        "interval": "1wk", 
        "period": "5y"
    }
)
investor.run()
```

## Configuration Parameters

### Core Parameters

- **`stocks`**: List of stock symbols to analyze (e.g., `['TSLA', 'AAPL', 'MSFT']`)
- **`patterns`**: List of pattern functions to apply (defaults to all available patterns)
- **`extra_params`**: Dictionary of additional configuration options

### Extra Parameters

- **`search_criteria`**: AI search criteria (e.g., `["rise_and_fall", "cup_and_handle"]`)
- **`interval`**: Data interval (`"1d"`, `"1wk"`, `"1mo"`)
- **`period`**: Analysis period (`"1y"`, `"2y"`, `"5y"`, `"max"`)

## Available Patterns

The library includes several built-in technical patterns:

- **`check_rise_then_fall`**: Identifies stocks that have risen significantly then fallen 50-75%
- **`check_weekly_rsi_low`**: Detects stocks with RSI below specified threshold (default: 30)

## Output

StockAxion generates comprehensive PDF reports that include:
- Stock analysis results
- Technical indicator charts
- Pattern recognition findings
- Investment recommendations

Reports are saved as `report.pdf` in the project directory.

## Project Structure

```
stockaxion/
├── api.py              # Main Investor API
├── stock_search.py     # AI-powered stock discovery
├── stock_filter.py     # Technical pattern filtering
├── reporting.py        # PDF report generation
├── indicators/
│   ├── pattern.py      # Technical pattern functions
│   └── price.py        # Price-based indicators
└── utils/
    ├── llm.py          # AI/LLM utilities
    └── generic.py      # General utilities
```

## Requirements

- Python 3.11+
- XAI API access
- Internet connection for stock data retrieval

## Contributing

Feel free to submit issues and enhancement requests!