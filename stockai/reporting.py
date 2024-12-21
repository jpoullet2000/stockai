from typing import List
from stockai.stock import Stock
from stockai.utils.llm import llm_client


class Report:
    """Reporting on a stock portfolio."""

    def __init__(self, stocks: List[str] | List[Stock]):
        if isinstance(stocks[0], str):
            stocks = [Stock(ticker_symbol) for ticker_symbol in stocks]
        self.stocks = stocks

    def _get_plot(self):
        for stock in self.stocks:
            stock.fetch_data(period="1y", interval="1d")
            stock.plot_data()

    def _get_reason_to_buy(self):
        """Get the reason to buy the stock."""
        for stock in self.stocks:
            prompt = f"Find the reasons to buy {stock.ticker_symbol}."
            completion = llm_client.chat.completions.create(
                model="grok-beta",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in stock markets.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            reason = completion.choices[0].message.content
            print(f"The reason to buy {stock.ticker_symbol} is: {reason}")

    def generate_report(self):
        """Generate a report on the stock portfolio.

        It should include the following information:
        - The plots of the stock prices.
        """
        self._get_plot()
        self._get_reason_to_buy()
