import yfinance as yf
import pandas as pd


class Stock:
    """A class to represent a stock."""

    def __init__(self, ticker_symbol: str, period: str = None, interval: str = None):
        self.ticker_symbol = ticker_symbol
        self._data = None
        self.period = period
        self.interval = interval

    def fetch_data(self, period: str, interval: str):
        """Fetch stock data using Yahoo Finance API.

        Args:
            period (str): The period for which to fetch the data (e.g., 1y).
            interval (str): The interval at which to fetch the data (e.g., 1wk).

        Returns:
            pd.DataFrame: The stock data as a pandas DataFrame.
        """
        self._data = yf.download(self.ticker_symbol, period=period, interval=interval)
        return self._data

    @property
    def data(self):
        if self._data is None:
            self._data = self.fetch_data(self.period, self.interval)
        return self._data

    def plot_data(self):
        """Plot the stock data."""
        self.data["Close"].plot()
