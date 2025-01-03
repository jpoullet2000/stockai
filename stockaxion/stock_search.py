from typing import List, Dict, Callable
import ast
from stockaxion.utils.llm import llm_client


class StockSearch(object):
    """Class to search for stocks ticker symbols based on some search criteria."""

    _search_methods: Dict[str, Callable] = {}

    @classmethod
    def register_search_method(cls, name: str):
        def decorator(func: Callable):
            cls._search_methods[name] = func
            return func

        return decorator

    def __init__(self):
        pass

    def search(
        self, search_criteria: List[str] | None = ["rise_and_fall"]
    ) -> List[str]:
        """Search for stocks based on the given search criteria.

        Args:
            search_criteria (str): The search criteria to use.

        Returns:
            List[str]: A list of stock ticker symbols that match the search criteria.
        """
        if search_criteria is None:
            search_criteria = ["rise_and_fall"]

        for criterion in search_criteria:
            if criterion not in self._search_methods:
                raise ValueError(
                    f"Invalid search criteria. Valid criteria are: {list(self._search_methods.keys())}"
                )

        results = []
        for criterion in search_criteria:
            results.extend(self._search_methods[criterion](self))

        return results


@StockSearch.register_search_method("cup_and_handle")
def _search_for_cup_and_handle(
    self,
) -> List[str]:
    """Search for stocks that have a cup and handle pattern.
    This call the LLM Grok model to get the stocks that match the search criteria.

    Returns:
        List[str]: A list of stock ticker symbols that match the search criteria.
    """
    prompt = (
        "Find stocks that have a cup and handle pattern. "
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


@StockSearch.register_search_method("rise_and_fall")
def _search_for_rise_and_fall(
    rise: int = 100,
    fall: int = 50,
    months=4,
    # self, rise: int = 100, fall: int = 50, months=4
) -> List[str]:
    """Search for stocks that have risen a lot then fallen 50-75% of the rise.
    This call the LLM Grok model to get the stocks that match the search criteria.


    Args:
        rise (int): The percentage rise in the stock price.
        fall (int): Thesearch_methods = {
        "rise_and_fall": self._search_for_rise_and_fall,
        # Add other criteria and corresponding methods here
    } percentage fall in the stock price.
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


VALID_SEARCH_CRITERIA = (
    StockSearch._search_methods
)  # ["rise_and_fall", "cup_and_handle"]
