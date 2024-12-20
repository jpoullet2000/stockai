from typing import List
import ast
from stockai.utils.llm import llm_client


VALID_SEARCH_CRITERIA = ["rise_and_fall"]


class StockSearch(object):
    """Class to search for stocks ticker symbols based on some search criteria."""

    def __init__(self):
        pass

    def search(self, search_criteria: str = "rise_and_fall") -> List[str]:
        """Search for stocks based on the given search criteria.

        Args:
            search_criteria (str): The search criteria to use.

        Returns:
            List[str]: A list of stock ticker symbols that match the search criteria.
        """
        if search_criteria == "rise_and_fall":
            return self._search_for_rise_and_fall()
        else:
            raise ValueError(
                f"Invalid search criteria. Valid criteria are: {VALID_SEARCH_CRITERIA}"
            )

    def _search_for_rise_and_fall(
        self, rise: int = 100, fall: int = 50, months=4
    ) -> List[str]:
        """Search for stocks that have risen a lot then fallen 50-75% of the rise.
        This call the LLM Grok model to get the stocks that match the search criteria.


        Args:
            rise (int): The percentage rise in the stock price.
            fall (int): The percentage fall in the stock price.
            months (int): The number of months in which the fall should occur.

        Returns:
            List[str]: A list of stock ticker symbols that match the search criteria.
        """
        prompt = (
            f"Find stocks that have risen {rise}% then fallen {fall}%. "
            f"The fall should occur in the last {months} months. "
            "For each stock, provide the ticker symbol "
            "such that the response should for instance be ['AAPL', 'GOOGL', 'AMZN'], no extra text. "
            "If you can provide 10 stocks, that would be great."
        )
        completion = llm_client.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "system", "content": "You are an expert in stock markets."},
                {"role": "user", "content": prompt},
            ],
        )
        return ast.literal_eval(completion.choices[0].message.content)
