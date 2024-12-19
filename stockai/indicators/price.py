import pandas as pd

def check_rise_then_fall(df, window_size=20, rise_threshold=100):
    """
    Check if the stock price has risen a lot then falls 50-75% of the rise within a rolling window.
    
    Args:
        df (pd.DataFrame): The stock data as a pandas DataFrame.
        window_size (int): The size of the rolling window.
       
    """
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
        return False

    # Check that the rolling sum has a peak > rise_threshold
    if rise_peak > rise_threshold:
        # Check that the rolling sum has a peak < fall_threshold
        if abs(fall_peak) > 0.25 * abs(rise_peak) and abs(fall_peak) < 0.5 * abs(rise_peak):
            return True
    return False
    

def estimate_rise(df):
    """This function estimates the highest rise
      in stock price during a window of at least 1 month.
      Depending on the interval of the stock data, the window size can be adjusted.

    Args:
        df (pd.DataFrame): The stock data as a pandas DataFrame.

    Returns:
        float: The highest rise in stock price.
    """
    # Calculate the percentage change in the stock price
    df["price_change"] = df["Close"].pct_change() * 100

    # Find the highest rise in stock price
    highest_rise = df["price_change"].max()

    return highest_rise
