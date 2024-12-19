#%% 
from stockai.utils.stock import fetch_stock_data

# Define the stock ticker symbol
ticker_symbol = 'ES.PA'  # Replace with the desired stock ticker
period='1y'
interval='1wk'

# Fetch the stock data
stock_data = fetch_stock_data(ticker_symbol, period, interval)


# %%
from stockai.indicators.price import check_rise_then_fall

# Check if the stock price has risen a lot then falls 50-75% of the rise
result = check_rise_then_fall(stock_data)
# %%
from stockai.indicators.price import estimate_rise
estimate_rise(stock_data)
# %%
