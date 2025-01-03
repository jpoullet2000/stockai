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