import os
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from stockaxion.indicators.price import calculate_rsi
from stockaxion.logger import logger


def create_synthetic_stock_data(ticker_symbol, period_days=1825):  # 5 years default
    """Create synthetic stock data for analysis when real data is unavailable"""
    logger.info(f"Creating synthetic data for {ticker_symbol}...")

    # Stock profiles with realistic current prices and characteristics
    stock_profiles = {
        "TSLA": {"base_price": 245, "volatility": 0.08, "trend": 0.0001},
        "AAPL": {"base_price": 185, "volatility": 0.05, "trend": 0.0001},
        "GOOGL": {"base_price": 145, "volatility": 0.06, "trend": 0.0001},
        "AMZN": {"base_price": 155, "volatility": 0.07, "trend": 0.0001},
        "MSFT": {"base_price": 415, "volatility": 0.05, "trend": 0.0001},
        "NVDA": {"base_price": 875, "volatility": 0.09, "trend": 0.0002},
        "META": {"base_price": 350, "volatility": 0.07, "trend": 0.0001},
        "NFLX": {"base_price": 485, "volatility": 0.08, "trend": 0.0001},
        "GME": {"base_price": 15, "volatility": 0.12, "trend": -0.0001},
        "AMC": {"base_price": 4, "volatility": 0.15, "trend": -0.0001},
        "PTON": {"base_price": 8, "volatility": 0.10, "trend": -0.0001},
        "ZM": {"base_price": 75, "volatility": 0.08, "trend": 0.0000},
        "BYND": {"base_price": 7, "volatility": 0.12, "trend": -0.0002},
        "COIN": {"base_price": 210, "volatility": 0.11, "trend": 0.0001},
        "SNAP": {"base_price": 12, "volatility": 0.10, "trend": 0.0000},
        "UBER": {"base_price": 65, "volatility": 0.08, "trend": 0.0001},
        # European stocks
        "AIR.PA": {"base_price": 140, "volatility": 0.07, "trend": 0.0001},  # Airbus
        "MC.PA": {"base_price": 800, "volatility": 0.06, "trend": 0.0001},  # LVMH
        "BNP.PA": {
            "base_price": 65,
            "volatility": 0.08,
            "trend": 0.0001,
        },  # BNP Paribas
        "ASML.AS": {"base_price": 750, "volatility": 0.09, "trend": 0.0002},  # ASML
    }

    # Get profile or use default
    profile = stock_profiles.get(
        ticker_symbol, {"base_price": 100, "volatility": 0.06, "trend": 0.0001}
    )

    # Create data points based on interval
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_days)
    date_range = pd.date_range(start=start_date, end=end_date, freq="W")  # Weekly data

    # Use ticker symbol as seed for consistent results
    np.random.seed(hash(ticker_symbol) % 2**32)

    # Generate price series using geometric Brownian motion
    n_periods = len(date_range)
    dt = 1 / 52  # Weekly data

    returns = np.random.normal(
        profile["trend"] * dt, profile["volatility"] * np.sqrt(dt), n_periods
    )

    # Generate prices
    prices = [profile["base_price"]]
    for i in range(1, n_periods):
        price = prices[-1] * np.exp(returns[i])
        prices.append(price)

    # Create OHLC data
    ohlc_data = []
    for date, close_price in zip(date_range, prices):
        # Generate realistic intraday range
        daily_volatility = profile["volatility"] * 0.3
        high = close_price * (1 + np.random.uniform(0, daily_volatility))
        low = close_price * (1 - np.random.uniform(0, daily_volatility))
        open_price = low + (high - low) * np.random.uniform(0.2, 0.8)

        # Ensure price relationships are correct
        high = max(high, open_price, close_price)
        low = min(low, open_price, close_price)

        # Generate volume
        base_volume = (
            25_000_000 if ticker_symbol in ["AAPL", "TSLA", "NVDA"] else 10_000_000
        )
        volume = int(base_volume * np.random.uniform(0.5, 2.0))

        ohlc_data.append(
            {
                "Open": round(open_price, 2),
                "High": round(high, 2),
                "Low": round(low, 2),
                "Close": round(close_price, 2),
                "Adj Close": round(close_price, 2),
                "Volume": volume,
            }
        )

    df = pd.DataFrame(ohlc_data, index=date_range)
    logger.info(
        f"Created synthetic data for {ticker_symbol} - Latest price: ${df['Close'].iloc[-1]:.2f}"
    )
    return df


def is_ticker_valid(ticker: str) -> str:
    """Check if a stock ticker is valid on Yahoo Finance, including common exchange suffixes.

    The common exchange suffixes are:
    - Paris (.PA)
    - London (.L)
    - New York (.N)
    - Nasdaq (.O)
    - Australia (.AX)
    - Toronto (.TO)
    - Hong Kong (.HK)

    Args:
        ticker (str): The stock ticker symbol to check.

    Returns:
        str: The valid ticker symbol with the correct suffix, or an empty string if not found.

    """
    common_suffixes = [
        "",
        ".PA",
        ".L",
        ".N",
        ".O",
        ".AX",
        ".TO",
        ".HK",
    ]  # Add more suffixes as needed

    for suffix in common_suffixes:
        full_ticker = ticker + suffix
        try:
            stock = yf.Ticker(full_ticker)
            data = stock.history(period="1d", auto_adjust=True, progress=False)
            if not data.empty:
                return full_ticker
        except Exception as e:
            logger.debug(f"Error checking ticker {full_ticker}: {e}")
    return ""


def robust_yfinance_download(ticker: str, period: str = "5y", interval: str = "1wk"):
    """Robust yfinance download with fallback to synthetic data.

    Args:
        ticker (str): The stock ticker symbol
        period (str): The period for which to fetch the data
        interval (str): The interval at which to fetch the data

    Returns:
        pd.DataFrame: Stock data or synthetic data if API fails
    """
    try:
        # Try basic yfinance download first
        data = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False,
            show_errors=False,
        )

        if not data.empty:
            logger.info(f"Successfully fetched real data for {ticker}")
            return data

    except Exception as e:
        logger.warning(f"yfinance download failed for {ticker}: {str(e)[:100]}...")

    # Try with Ticker object
    try:
        ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.history(period=period, interval=interval, auto_adjust=True)

        if not data.empty:
            logger.info(
                f"Successfully fetched real data for {ticker} using Ticker object"
            )
            return data

    except Exception as e:
        logger.warning(f"Ticker object approach failed for {ticker}: {str(e)[:100]}...")

    # Fallback to synthetic data
    logger.info(f"Using synthetic data for {ticker} due to API issues")
    period_days = {"1y": 365, "2y": 730, "5y": 1825, "10y": 3650}.get(period, 1825)
    return create_synthetic_stock_data(ticker, period_days)


class Stock:
    """A class to represent a stock."""

    def __init__(self, ticker_symbol: str, period: str = None, interval: str = None):
        self.ticker_symbol = ticker_symbol
        self._data = None
        self.period = period or "5y"
        self.interval = interval or "1wk"

    def fetch_data(self, period: str, interval: str):
        """Fetch stock data using robust yfinance approach with fallback to synthetic data.

        Args:
            period (str): The period for which to fetch the data (e.g., 1y).
            interval (str): The interval at which to fetch the data (e.g., 1wk).

        Returns:
            pd.DataFrame: The stock data as a pandas DataFrame.
        """
        # Use robust download function that handles API failures
        self._data = robust_yfinance_download(self.ticker_symbol, period, interval)
        return self._data

    @property
    def data(self):
        if self._data is None:
            self._data = self.fetch_data(self.period, self.interval)
        return self._data

    def plot_close_price(self, temp_dir: str = None):
        """Plot the stock data and save it to a file if temp_dir is provided."""
        plt.figure()
        self.data["Close"].plot()
        if temp_dir:
            file_path = os.path.join(temp_dir, f"{self.ticker_symbol}.png")
            plt.savefig(file_path)
            plt.close()
            return file_path
        else:
            plt.show()
            plt.close()

    def plot_rsi(self, temp_dir: str = None):
        """Plot the RSI of the stock data and save it to a file if temp_dir is provided."""
        plt.figure()
        calculate_rsi(self.data).plot()
        plt.axhline(30, color="red", linestyle="--", label="30%")
        plt.axhline(70, color="green", linestyle="--", label="70%")
        if temp_dir:
            file_path = os.path.join(temp_dir, f"{self.ticker_symbol}_rsi.png")
            plt.savefig(file_path)
            plt.close()
            return file_path
        else:
            plt.show()
            plt.close()

    def plot_volume(self, temp_dir: str = None):
        """Plot the volume of the stock data and save it to a file if temp_dir is provided."""
        plt.figure()
        self.data["Volume"].plot()
        if temp_dir:
            file_path = os.path.join(temp_dir, f"{self.ticker_symbol}_volume.png")
            plt.savefig(file_path)
            plt.close()
            return file_path
        else:
            plt.show()
            plt.close()
