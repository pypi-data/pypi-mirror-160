import json
import re
from typing import Any, Dict, List

from bs4 import BeautifulSoup as bs
from dataproc.crawlers import fetch


def extract_data(soup) -> List[Dict[str, Any]]:
    """ Parse js script tags and try to get javascript objects 
    a.k.a json """
    data = []
    for ix, s in enumerate(soup.find_all('script')):
        # print(s.string)
        # print(type(str(s.string)))
        parsed = re.findall(r"{.+[:,].+}|\[.+[,:].+\]", str(s.string))
        try:
            if parsed:
                _d = json.loads(parsed[0])
                # print(ix, json.loads(parsed[0]))
                data.append(_d)
        except json.JSONDecodeError:
            pass
    return data


def get_video(url: str, strategy="direct", ix=1) -> Dict[str, Any]:
    """ extracts metadata info from a youtube link """
    req = fetch.from_url(url)
    req.strategy = strategy
    rsp = fetch.get(req)

    soup = bs(rsp.text)
    data = extract_data(soup)
    video = data[ix]["videoDetails"]
    return video
