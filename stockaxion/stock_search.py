from typing import List, Dict, Callable
import ast
import os
from stockaxion.utils.llm import llm_client


class StockSearch(object):
    """Class to search for stocks ticker symbols based on some search criteria."""

    _search_methods: Dict[str, Callable] = {}

    # Class-level blacklist for permanently excluded tickers
    _blacklisted_tickers: List[str] = [
        # Add tickers you want to permanently exclude
        # Example: "PENN", "SPCE", "GME", "AMC"
    ]

    @classmethod
    def register_search_method(cls, name: str):
        def decorator(func: Callable):
            cls._search_methods[name] = func
            return func

        return decorator

    @classmethod
    def add_to_blacklist(cls, tickers: List[str]):
        """Add tickers to the permanent blacklist.

        Args:
            tickers (List[str]): List of ticker symbols to blacklist.
        """
        cls._blacklisted_tickers.extend([ticker.upper() for ticker in tickers])
        # Remove duplicates
        cls._blacklisted_tickers = list(set(cls._blacklisted_tickers))

    @classmethod
    def remove_from_blacklist(cls, tickers: List[str]):
        """Remove tickers from the permanent blacklist.

        Args:
            tickers (List[str]): List of ticker symbols to remove from blacklist.
        """
        remove_upper = [ticker.upper() for ticker in tickers]
        cls._blacklisted_tickers = [
            ticker
            for ticker in cls._blacklisted_tickers
            if ticker.upper() not in remove_upper
        ]

    @classmethod
    def get_blacklist(cls) -> List[str]:
        """Get the current blacklist.

        Returns:
            List[str]: Current blacklisted tickers.
        """
        return cls._blacklisted_tickers.copy()

    def __init__(self):
        pass

    def search(
        self,
        search_criteria: List[str] | None = ["rise_and_fall"],
        exclude_tickers: List[str] | None = None,
    ) -> List[str]:
        """Search for stocks based on the given search criteria.

        Args:
            search_criteria (str): The search criteria to use.
            exclude_tickers (List[str], optional): List of ticker symbols to exclude from results.

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

        # Combine exclusion lists (blacklist + temporary exclusions)
        all_exclusions = self._blacklisted_tickers.copy()
        if exclude_tickers:
            all_exclusions.extend(exclude_tickers)

        for criterion in search_criteria:
            results.extend(
                self._search_methods[criterion](self, exclude_tickers=all_exclusions)
            )

        # Remove duplicates and filter out any remaining excluded tickers (as backup)
        unique_results = list(set(results))
        print(f"DEBUG: Before exclusion filtering: {unique_results}")
        print(f"DEBUG: All exclusions: {all_exclusions}")

        if all_exclusions:
            # Convert to uppercase for case-insensitive comparison
            exclude_upper = [ticker.upper() for ticker in all_exclusions]
            filtered_results = [
                ticker
                for ticker in unique_results
                if ticker.upper() not in exclude_upper
            ]
            print(f"DEBUG: After exclusion filtering: {filtered_results}")
            return filtered_results

        return unique_results


@StockSearch.register_search_method("cup_and_handle")
def _search_for_cup_and_handle(self, exclude_tickers: List[str] = None) -> List[str]:
    """Search for stocks that have a cup and handle pattern.
    This call the LLM Grok model to get the stocks that match the search criteria.

    Args:
        exclude_tickers (List[str], optional): List of ticker symbols to exclude from results.

    Returns:
        List[str]: A list of stock ticker symbols that match the search criteria.
    """
    prompt = (
        "Find stocks that have a cup and handle pattern. "
        "For each stock, provide the ticker symbol "
        "such that the response should for instance be ['AAPL', 'GOOGL', 'AMZN'], no extra text. "
        "If you can provide 10 stocks, that would be great."
    )

    # Add exclusion instruction to prompt if there are tickers to exclude
    if exclude_tickers:
        exclude_str = ", ".join(exclude_tickers)
        prompt += f"\n\nIMPORTANT: Do NOT include any of these tickers in your response: {exclude_str}"

    completion = llm_client.chat.completions.create(
        # model="grok-beta",
        model=os.getenv("LLM_MODEL"),
        messages=[
            {"role": "system", "content": "You are an expert in stock markets."},
            {"role": "user", "content": prompt},
        ],
    )
    result = ast.literal_eval(completion.choices[0].message.content)
    return result


@StockSearch.register_search_method("rise_and_fall")
def _search_for_rise_and_fall(
    self, exclude_tickers: List[str] = None, rise: int = 100, fall: int = 50, months=4
) -> List[str]:
    """Search for stocks that have risen a lot then fallen 50-75% of the rise.
    This call the LLM Grok model to get the stocks that match the search criteria.

    Args:
        exclude_tickers (List[str], optional): List of ticker symbols to exclude from results.
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

    # Add exclusion instruction to prompt if there are tickers to exclude
    if exclude_tickers:
        exclude_str = ", ".join(exclude_tickers)
        prompt += f"\n\nIMPORTANT: Do NOT include any of these tickers in your response: {exclude_str}"

    completion = llm_client.chat.completions.create(
        # model="grok-beta",
        model=os.getenv("LLM_MODEL"),
        messages=[
            {"role": "system", "content": "You are an expert in stock markets."},
            {"role": "user", "content": prompt},
        ],
    )
    return ast.literal_eval(completion.choices[0].message.content)


VALID_SEARCH_CRITERIA = (
    StockSearch._search_methods
)  # ["rise_and_fall", "cup_and_handle"]
