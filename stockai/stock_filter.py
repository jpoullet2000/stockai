from typing import List
import stockai.indicators.pattern as pattern_module
from stockai.indicators.pattern import Pattern
from stockai.stock import Stock
from stockai.logger import logger


class StockFilter:
    """Filter stocks based on various criteria

    From the list of stocks, keep only those which follow the given patterns.
    """

    def __init__(
        self,
        stocks: List[str] | List[Stock],
        patterns: List[str] | List[Pattern],
        extra_params: dict = {},
    ):
        self.extra_params = extra_params
        self.stocks = self._get_stocks(stocks)
        self.patterns = self._get_patterns(patterns)

    def _get_stocks(self, stocks: List[str] | List[Stock]) -> List[Stock]:
        """Get the stock objects from the given list of stock ticker symbols.

        Args:
            stocks (List[str] | List[Stock]): A list of stock ticker symbols or stock objects.

        Returns:
            List[Stock]: A list of stock objects.
        """
        stock_objects = []
        for stock in stocks:
            if isinstance(stock, str):
                period = self.extra_params.get("period")
                interval = self.extra_params.get("interval")
                stock_objects.append(
                    Stock(ticker_symbol=stock, period=period, interval=interval)
                )
            elif isinstance(stock, Stock):
                stock_objects.append(stock)
            else:
                raise ValueError("Invalid stock")
        return stock_objects

    def _get_patterns(self, patterns: List[str] | List[Pattern]) -> List[Pattern]:
        """Get the pattern objects from the given list of patterns.

        Args:
            patterns (List[str] | List[Pattern]): A list of pattern names or pattern objects.

        Returns:
            List[Pattern]: A list of pattern objects.
        """
        pattern_objects = []
        for pattern in patterns:
            if isinstance(pattern, str):
                pattern_function = getattr(pattern_module, pattern)
                pattern_objects.append(Pattern(name=pattern, function=pattern_function))
            elif isinstance(pattern, Pattern):
                pattern_objects.append(pattern)
            else:
                raise ValueError("Invalid pattern")
        return pattern_objects

    def filter(self) -> List[str]:
        """Filter the stocks based on the given patterns.

        Returns:
            List[str]: A list of stock ticker symbols that match all the patterns.
        """
        filtered_stocks = []
        for stock in self.stocks:
            all_patterns_matched = True
            for pattern in self.patterns:
                if not pattern.check(stock.data):
                    logger.info(f"{stock.ticker_symbol} does not match {pattern.name}")
                    all_patterns_matched = False
                    break
            if all_patterns_matched:
                logger.info(f"{stock.ticker_symbol} matches all patterns")
                filtered_stocks.append(stock.ticker_symbol)
        return filtered_stocks
