import requests
from bs4 import BeautifulSoup
import pandas_datareader as pdr


class StooqUrlFactory:
    root = "https://stooq.pl/"

    def build_url(self, *parts):
        to_append = "/".join(parts)
        return self.root + to_append


class TickerPage:
    url_components: list = ["q", "i", "?s=^spx&l="]

    def __init__(self, factory=StooqUrlFactory()):
        self.factory: StooqUrlFactory = factory
        self._tickers: list = []

    def __str__(self):
        return f"TickerPage object with {len(self.tickers)} tickers loaded"

    @property
    def tickers(self):
        return self._tickers

    def add_tickers(self, new_tickers):
        self._tickers += new_tickers

    def get_html(self, index) -> str:
        url = self.factory.build_url(*self.url_components) + str(index)
        response = requests.get(url, verify=False)
        return response.text

    def retrieve_tickers(self, index, parser="lxml") -> list:
        tickers = []
        html_content = self.get_html(index)
        soup = BeautifulSoup(html_content, parser)
        table = soup.find("table", {"id": "fth1"}).find("tbody")

        for row in table.find_all("tr"):
            try:
                ticker_cell = row.find("td")
                ticker = ticker_cell.text
                formatted_ticker = ticker[:-3]
            except (AttributeError, IndexError):
                formatted_ticker = ""

            tickers.append(formatted_ticker)

        return tickers


class ContextManager:
    """Object that interfaces TickerPage to automatically generate tickers without explicitly checking for the number
    of available pages"""
    tp = TickerPage()

    def gen_tickers(self) -> list:
        i = 1
        while True:

            ticker_list = self.tp.retrieve_tickers(i)
            if not ticker_list:
                break  # no more tickers to scrape
            self.tp.add_tickers(new_tickers=ticker_list)
            i += 1

        return self.tp.tickers


class TimeSeriesDownloader:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_time_series(self, ticker: str):
        """Dla danego tickera funkcja pobierze notowania na zadany w konstruktorze okres czasu"""
        df = pdr.DataReader(ticker, 'yahoo', self.start, self.end)
        df = df["Adj Close"]  # bierzemy tylko kolumnę Adjusted Close
        df = df.rename(ticker)
        return df


class DownloadManager:
    def __init__(self, ts_downloader):
        self.ts_downloader: TimeSeriesDownloader = ts_downloader
        self.all_dfs = []

    def download_data(self, ticker):
        df = self.ts_downloader.get_time_series(ticker)
        self.all_dfs.append(df)

