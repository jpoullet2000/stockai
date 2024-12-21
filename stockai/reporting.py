from typing import List
from stockai.stock import Stock
from stockai.utils.llm import llm_client
from fpdf import FPDF
import markdown2
import tempfile
from tempfile import TemporaryDirectory

TEMP_DIR = TemporaryDirectory()


class PDF(FPDF):
    def add_chapter(self, title, content):
        self.add_page()
        self.set_font("Arial", style="B", size=16)
        self.cell(
            0,
            10,
            title.encode("latin-1", "replace").decode("latin-1"),
            ln=True,
            align="C",
        )
        self.ln(10)
        self.set_font("Arial", size=12)
        self.multi_cell(0, 10, content.encode("latin-1", "replace").decode("latin-1"))


class Report:
    """Reporting on a stock portfolio."""

    def __init__(
        self,
        stocks: List[str] | List[Stock],
        output_file: str = "report.pdf",
        extra_params: dict = {},
    ):
        if isinstance(stocks[0], str):
            stocks = [Stock(ticker_symbol) for ticker_symbol in stocks]
        self.stocks = stocks
        self.output_file = output_file
        self.extra_params = extra_params

    def _display_plots(self):
        for stock in self.stocks:
            stock.fetch_data(
                period=self.extra_params.get("period", "1y"),
                interval=self.extra_params.get("interval", "1d"),
            )
            stock.plot_data()

    def _get_plot(self, stock, temp_dir):
        """Get the plot of the stock prices."""
        stock.fetch_data(
            period=self.extra_params.get("period", "1y"),
            interval=self.extra_params.get("interval", "1d"),
        )
        plot_path = stock.plot_data(temp_dir=temp_dir)
        return plot_path

    def _get_reason_to_buy(self, stock):
        """Get the reason to buy the stock."""
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
        return completion.choices[0].message.content

    def _get_reason_to_buy_all_stocks(self):
        """Get the reason to buy the stock."""
        for stock in self.stocks:
            reason = self._get_reason_to_buy(stock)
            print(f"The reason to buy {stock.ticker_symbol} is: {reason}")

    def generate_report(self):
        """Generate a report on the stock portfolio.

        It should include the following information:
        - The plots of the stock prices.
        """
        self._get_plot()
        self._get_reason_to_buy()

    def save_report(self):
        """Save the report to a PDF file."""

        with tempfile.TemporaryDirectory() as temp_dir:
            pdf = PDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", style="B", size=16)
            pdf.cell(
                200,
                10,
                "Stock Portfolio Report".encode("latin-1", "replace").decode("latin-1"),
                ln=True,
                align="C",
            )
            pdf.set_font("Arial", size=12)
            pdf.ln(10)
            pdf.cell(
                200,
                10,
                "Stock Prices".encode("latin-1", "replace").decode("latin-1"),
                ln=True,
            )

            for stock in self.stocks:
                plot_path = self._get_plot(stock, temp_dir)
                reason_to_buy = self._get_reason_to_buy(stock)
                reason_to_buy_html = markdown2.markdown(reason_to_buy)
                reason_to_buy_text = self._html_to_text(reason_to_buy_html)
                content = f"Reason to buy {stock.ticker_symbol}:\n{reason_to_buy_text}"
                pdf.add_chapter(stock.ticker_symbol, content)
                pdf.image(plot_path, x=10, w=190)

            pdf.output(self.output_file)

    def _html_to_text(self, html):
        """Convert HTML content to plain text with basic formatting."""
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text("\n")
        # Remove leading colons
        text = text.replace("\n:", "\n")
        return text
