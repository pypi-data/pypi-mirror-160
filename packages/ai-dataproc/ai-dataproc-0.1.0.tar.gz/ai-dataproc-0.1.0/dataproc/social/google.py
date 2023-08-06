import json
from dataclasses import dataclass
from typing import List, Optional, Tuple

import requests
from pytrends.request import TrendReq


@dataclass
class Options:
    tz: int = 0
    timeout: Tuple[int, int] = (10, 25)
    retries: int = 2
    backoff: float = 0.1
    hl: Optional[str] = None



class GTrends:

    _fox_headers = {
        "Host": "trends.google.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "TE": "Trailers",
    }
    _global_trends = "https://trends.google.com/trends/api/topdailytrends?hl=en-US&tz=180&geo=IS"

    def __init__(self, opts: Options):
        self.api = TrendReq(tz=opts.tz,
                            timeout=opts.timeout,
                            retries=opts.retries,
                            backoff_factor=opts.backoff
                            )

    @classmethod
    def from_default(cls):
        opt = Options()
        return cls(opt)

    def trends_by_region(self, country) -> List[str]:
        """
        Available regions depends on the list of this url:

        https://trends.google.com/trends/hottrends/visualize/internal/data
        """
        if country == "global":
            words = self.trends_global()
        else:
            df = self.api.trending_searches(pn=country)
            words = df[0].to_list()

        return words

    def get_global(self, hl="en-US", tz=180, geo="IS", trim_chars=6):
        """
        Gets global trends by country
        :param hl: will be the language, but really it conservs the original lang of the keyword. 
        I think this param is more related to the UI lang. 
        :param tz: Is not standard, 180 is UTC.
        :param geo: Another not standard field, this is for geolocation response, 
        in this case doesn't matter.
        :param trim_chars: the response start with  ")]}\"
        url: https://trends.google.com/trends/api/topdailytrends?hl=en-US&tz=180&geo=Global
        """
        url = f"https://trends.google.com/trends/api/topdailytrends?hl={hl}&tz={tz}&geo={geo}"

        s = requests.session()
        s.headers = self._fox_headers

        rsp = s.get(self._global_trends, headers=self._fox_headers)
        text = rsp.text[trim_chars:]
        return json.loads(text)

    def trends_all(self):
        """
        The response to this url:
        https://trends.google.com/trends/hottrends/visualize/internal/data
        is a json with the main keywords for each country.
        The list of countries is not complete. 
        """
        url = "https://trends.google.com/trends/hottrends/visualize/internal/data"
        s = requests.session()

        rsp = s.get(self._global_trends, headers=self._fox_headers)
        return rsp.json()

    def trends_global(self):
        """
        It only get the words from the front panel.
        """
        data = self.get_global()
        words = [x["title"] for x in data["default"]["trendingSearches"]]
        return words
