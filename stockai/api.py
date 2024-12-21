from typing import List
from stockai.stock_search import StockSearch
from stockai.stock_filter import StockFilter
from stockai.reporting import Report
from stockai.indicators.pattern import get_all_pattern_functions


class Investor:
    def __init__(
        self,
        patterns: List[str] = None,
        stocks: List[str] = None,
        extra_params: dict = {},
    ):
        self.stocks = stocks
        self.patterns = patterns or get_all_pattern_functions()
        self.extra_params = extra_params

    def run(self):
        """First get stocks from the stock search, then filter the stocks
        based on the given patterns and finally generate a report."""
        if not self.stocks:
            search_criteria = self.extra_params.get("search_criteria")
            self.stocks = StockSearch(search_criteria).search()
        filtered_stocks = StockFilter(
            stocks=self.stocks, patterns=self.patterns, extra_params=self.extra_params
        ).filter()
        report = Report(stocks=filtered_stocks, extra_params=self.extra_params)
        report.save_pdf_report()
