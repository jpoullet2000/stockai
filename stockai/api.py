from typing import List
from stockai.stock_search import StockSearch
from stockai.stock_filter import StockFilter
from stockai.reporting import Report
from stockai.indicators.pattern import get_all_pattern_functions
from stockai.logger import logger


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

    def run(self, use_filters: bool = True):
        """First get stocks from the stock search, then filter the stocks
        based on the given patterns and finally generate a report."""
        if not self.stocks:
            logger.info("No stocks provided. Searching for stocks...")
            search_criteria = self.extra_params.get("search_criteria")
            self.stocks = StockSearch().search(search_criteria)
            logger.info(f"Found {len(self.stocks)} stocks: {self.stocks}")

        if not use_filters:
            logger.info("Skipping filters")
            filtered_stocks = self.stocks
        else:
            logger.info(f"Filtering stocks based on patterns: {self.patterns}")
            filtered_stocks = StockFilter(
                stocks=self.stocks,
                patterns=self.patterns,
                extra_params=self.extra_params,
            ).filter()
            logger.info(
                f"Found {len(filtered_stocks)} stocks after filtering: {filtered_stocks}"
            )
        if not filtered_stocks:
            logger.info("No stocks found")
            return
        logger.info("Generating report...")
        report = Report(stocks=filtered_stocks, extra_params=self.extra_params)
        report.save_pdf_report()
        logger.info("Report generated successfully. Report available at: report.pdf")
        return report
