# stockaxion
Find opportunity to invest in stocks

## Get started

Add your XAI API key in .env 

```
XAI_API_KEY=<xai_api_key>
```

To run your analysis 

```python
from stockaxion.api import Investor
investor = Investor()
investor.run()
```

If you want to specify a search criterion, say you're looking for a cup and handle pattern, 

```python
investor = Investor(extra_params={"search_criteria": ["cup_and_handle"]})
investor.run(use_filters=False)
```
The `use_filters=False` option means that no filter will be applied to the results of the stock search, typically 10 stock tickers.

You can also specify the stocks you want to analyze with the `stocks` argument.  

```python
investor = Investor(
    stocks=['TSLA', 'RIVN', 'PLTR', 'ROKU'],
    patterns=["check_rise_then_fall"],
    extra_params={
        "search_criteria": ["rise_and_fall"], 
        "interval": "1wk", 
        "period": "5y"
    }
)
investor.run()
```
with 

- stocks: A list of stock symbols to analyze (e.g., Tesla, Rivian, Palantir, Roku).
- patterns: A list of patterns to check for in the stock data (e.g., "check_rise_then_fall").
- extra_params: Additional parameters for the analysis:
    - search_criteria: Criteria for the search (e.g., "rise_and_fall").
    - interval: The time interval for the data (e.g., "1 week").
    - period: The period over which to analyze the data (e.g., "5 years").