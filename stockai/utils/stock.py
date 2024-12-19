import yfinance as yf
import pandas as pd


def filter_stocks():
    """
    """
    pass

def fetch_stock_data(ticker_symbol: str, period: str, interval: str) -> pd.DataFrame:
    """Fetch stock data using Yahoo Finance API.
    
    Args:
        ticker_symbol (str): The stock ticker symbol.
        period (str): The period for which to fetch the data (e.g., 1y).
        interval (str): The interval at which to fetch the data (e.g., 1wk).
    
    Returns:
        pd.DataFrame: The stock data as a pandas DataFrame.

    Example:
        >>> fetch_stock_data("AAPL", "1y", "1d")
    """
    stock_data = yf.download(ticker_symbol, period=period, interval=interval)
    return stock_data

