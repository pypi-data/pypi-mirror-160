from typing import List

import pandas as pd  # library for data analysis
from bs4 import BeautifulSoup  # library to parse HTML documents
from dataproc.crawlers import fetch


class WikiTables:
    """ Crawl tables from a wikipedia url """

    def __init__(self, url: str, strategy="direct"):
        self.tables: List[str] = []
        self._url = url
        self._soup = None
        self._strategy = strategy
        self.get(url)

    def get(self, url: str):
        req = fetch.from_url(url)
        req.strategy = self._strategy
        r = fetch.get(req)
        self._soup = BeautifulSoup(r.text, "lxml")
        self.tables = self._soup.find_all('table', {'class': "wikitable"})

    def to_pandas(self, ix: int) -> pd.DataFrame:
        df = pd.read_html(str(self.tables[ix]))
        df = pd.DataFrame(df[0])
        return df


def get_table(url, ix) -> pd.DataFrame:
    """ Shorthand when you know which table do you want. """
    wt = WikiTables(url)
    return wt.to_pandas(ix)
