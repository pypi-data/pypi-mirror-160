import urllib.robotparser
from datetime import datetime
from typing import List, Optional

from bs4 import BeautifulSoup
from dataproc.crawlers import fetch
from dateutil.parser import parse as dtparser
from reppy.robots import Robots

# https://practicaldatascience.co.uk/data-science/how-to-scrape-open-graph-protocol-data-using-python
# https://www.codegrepper.com/code-examples/python/retrieve++all+meta+tags+python+beautifulsoup
# url = # sys.argv[1]


def difference_from_now(dt: str):
    now = datetime.utcnow()
    _dt = dtparser(dt, ignoretz=True)
    diff = now - _dt
    return diff


def date_parser(dt: str, ignoretz=True):
    try:
        _dt: Optional[datetime] = dtparser(dt, ignoretz=ignoretz)
    except ValueError:
        _dt = None
    except TypeError:
        _dt = None
    return _dt


def fetch_site(url):
    req = fetch.from_url(url)
    try:
        rsp = fetch.get(req)
        soup = BeautifulSoup(rsp.text, 'lxml')
        return soup
    except:
        return None


def parse_xml(urls):
    final = []
    for u in urls:
        lastmod = u.find("lastmod")
        lastmod_txt = ""
        if lastmod:
            lastmod_txt = lastmod.text

        data = dict(fullurl=u.find("loc").text,
                    lastmod=lastmod_txt)
        final.append(data)

    return final


def parser_robot(u):
    # rp = urllib.robotparser.RobotFileParser()
    robot_url = f"{u}/robots.txt"
    rp = Robots.fetch(robot_url)
    sitemaps = rp.sitemaps
    # rp.set_url(robot_url)
    # rp.read()
    # sitemaps = rp.site_maps()
    return sitemaps


def get_sitemaps_from_url(url: str) -> List[str]:
    robot_url = f"{url}/robots.txt"
    req = fetch.from_url(robot_url)
    rsp = fetch.get(req)
    sitemaps = []
    for line in rsp.text.splitlines():
        if "Sitemap:" in line:
            sitemaps.append(line.split()[1])
    return sitemaps


def parse_sites_xml(sitesxml: List[str], filter_dt=1):
    """
    :param filter_dt: filter sitemaps below 1 day
    """

    total_sites = []
    for s in sitesxml:
        print("Parsing ", s)
        soup = fetch_site(s)
        if soup:
            urls = soup.findAll("url")
            if urls:
                sites = parse_xml(urls)
                total_sites.extend(sites)
            else:
                # breakpoint()
                # locs = s.findAll("loc")
                # for l in locs:
                xmlsites = soup.findAll("sitemap")
                for s in xmlsites:
                    try:
                        diff = difference_from_now(s.lastmod.text)
                        if diff.days <= filter_dt:
                            _soup = fetch_site(s.loc.text)
                            if _soup:
                                _urls = _soup.findAll("url")
                                sites = parse_xml(_urls)
                                total_sites.extend(sites)
                    except AttributeError:
                        pass
    return total_sites
