from dataclasses import dataclass
from datetime import datetime
from typing import Optional


from newspaper import Article


@dataclass
class ArticleData:
    url: str
    text: str
    publish_date: Optional[datetime]

    @classmethod
    def from_html(cls, url: str, html: str):
        a = Article(url=url)
        a.download(input_html=html)
        a.parse()
        return cls(url=url, text=a.text, publish_date=a.publish_date)


