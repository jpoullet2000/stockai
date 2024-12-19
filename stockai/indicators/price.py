import pandas as pd

def check_rise_then_fall(df, window_size=20):
    """
    Check if the stock price has risen a lot then falls 50-75% of the rise within a rolling window.
    
    Args:
        df (pd.DataFrame): The stock data as a pandas DataFrame.
        window_size (int): The size of the rolling window.
       
    """
    # Calculate the percentage change in the stock price
    df["price_change"] = df["Close"].pct_change() * 100
    
    # Calculate rolling maximum and minimum percentage change
    df["rolling_max"] = df["price_change"].rolling(window=window_size).max()
    df["rolling_min"] = df["price_change"].rolling(window=window_size).min()
    
    # Check for a rise greater than 10% and a fall of 50-75% of the rise within the rolling window
    for i in range(len(df)):
        if df["rolling_max"].iloc[i] > 10:
            rise = df["rolling_max"].iloc[i]
            fall = df["rolling_min"].iloc[i]
            if fall < -0.5 * rise and fall > -0.75 * rise:
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
