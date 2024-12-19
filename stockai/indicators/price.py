def check_rise_then_fall(df):
    """
    Check if the stock price has risen a lot then falls 50-75% of the rise.
    
    Args:
        df (pd.DataFrame): The stock data as a pandas DataFrame.
       
    """
    # Calculate the percentage change in the stock price
    df["price_change"] = df["Close"].pct_change() * 100
    
    # Check if the stock price has risen a lot then falls 50-75% of the rise
    if df["price_change"].max() > 10 and df["price_change"].min() < -50:
        return True
    else:
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

