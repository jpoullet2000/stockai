# stockaxion
Find opportunity to invest in stocks

## Get started

Add your XAI API key in .env 

```
XAI_API_KEY=<xai_api_key>
```

To run your analysis 

```python
from stockai.api import Investor
investor = Investor()
investor.run()
```

If you want to specify a search criterion, say you're looking for a cup and handle pattern, 

```
investor = Investor(extra_params={"search_criteria": ["cup_and_handle"]})
investor.run(use_filters=False)
```
The `use_filters=False` option means that no filter will be applied to the results of the stock search, typically 10 stock tickers.

You can also specify the stocks you want to analyze with the `stocks` argument.  

```
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
