import pandas as pd
import inspect
from stockaxion.logger import logger
from stockaxion.indicators.price import calculate_rsi


class Pattern:
    def __init__(self, name: str, function):
        self.name = name
        self.function = function

    def check(self, df, **kwargs):
        return self.function(df, **kwargs)


def check_rise_then_fall(df, window_size=20, rise_threshold=100):
    """
    Check if the stock price has risen a lot then falls 50-75% of the rise within a rolling window.

    Args:
        df (pd.DataFrame): The stock data as a pandas DataFrame.
        window_size (int): The size of the rolling window.

    """
    if df.empty:
        logger.info("Empty DataFrame")
        return False
    # Calculate the percentage change in the stock price
    df["price_change"] = df["Close"].pct_change() * 100

    # Calculate rolling maximum and minimum percentage change
    # Calculate the rolling sum of percentage changes
    df["rolling_sum"] = df["price_change"].rolling(window=window_size).sum()
    rise_peak = df["rolling_sum"].max()
    fall_peak = df["rolling_sum"].min()

    # Check that the rise occurs before the fall in the rolling sum
    rise_index = df["rolling_sum"].idxmax()
    fall_index = df["rolling_sum"].idxmin()
    if rise_index > fall_index:
        logger.info("Rise occurs after fall")
        return False
    # Also check that the fall occurs in the last quarter of the whole period (not just the rolling window)
    if fall_index < df.index[len(df) - len(df) // 4]:
        logger.info("Fall occurs too early")
        return False

    # Check that the rolling sum has a peak > rise_threshold
    if rise_peak > rise_threshold:
        # Check that the rolling sum has a peak < fall_threshold
        if abs(fall_peak) > 0.25 * abs(rise_peak) and abs(fall_peak) < 0.5 * abs(
            rise_peak
        ):
            return True
    logger.info("Rise or fall peak not within threshold")
    return False


def check_weekly_rsi_low(df, window_size=14, rsi_threshold=30):
    """
    Check if the RSI of the stock is below a certain threshold
    within a rolling window in the last month of the period.

    Args:
        df (pd.DataFrame): The stock data as a pandas DataFrame.
        window_size (int): The size of the rolling window.

    """
    # Calculate the RSI of the stock
    rsi = calculate_rsi(df, window=window_size)

    # Check if the RSI is below the threshold in the last month of the period
    last_month = rsi.index[-1] - pd.DateOffset(months=1)
    rsi_last_month = rsi[rsi.index >= last_month]
    if any((rsi_last_month < rsi_threshold).values):
        return True
    return False


# def get_all_pattern_functions():
#     """Returns a list of all functions defined in the pattern module."""
#     current_module = inspect.getmodule(get_all_pattern_functions)
#     functions = []
#     for name, obj in inspect.getmembers(current_module):
#         if inspect.isfunction(obj) and obj.__module__ == current_module.__name__:
#             functions.append(obj)
#     return functions


def get_all_pattern_functions():
    """Returns a list of all functions defined in the pattern module, excluding itself."""
    current_module = inspect.getmodule(get_all_pattern_functions)
    functions = []
    for name, obj in inspect.getmembers(current_module):
        if (
            inspect.isfunction(obj)
            and obj.__module__ == current_module.__name__
            and name != "get_all_pattern_functions"
        ):
            functions.append(obj)
    return functions


# def get_all_pattern_functions():
#     """Returns a list of all functions defined in this module."""
#     functions = []
#     for name, obj in inspect.getmembers(inspect.getmodule(get_all_pattern_functions)):
#         if inspect.isfunction(obj):
#             functions.append(obj)
#     return functions
