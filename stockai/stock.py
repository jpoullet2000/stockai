import yfinance as yf
import pandas as pd

class Stock:
    """A class to represent a stock."""

    def __init__(self, ticker_symbol: str):
        self.ticker_symbol = ticker_symbol
        self.data = None
    
    def fetch_data(self, period: str, interval: str):
        """Fetch stock data using Yahoo Finance API.
        
        Args:
            period (str): The period for which to fetch the data (e.g., 1y).
            interval (str): The interval at which to fetch the data (e.g., 1wk).
        
        Returns:
            pd.DataFrame: The stock data as a pandas DataFrame.
        """
        self.data = yf.download(self.ticker_symbol, period=period, interval=interval)
        return self.data
    
    def plot_data(self):
        """Plot the stock data.
        """
        if self.data is not None:
            self.data["Close"].plot()
        else:
            print("No data available. Please fetch the data first.")

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

