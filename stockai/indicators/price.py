def calculate_rsi(data, window=14):
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


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
