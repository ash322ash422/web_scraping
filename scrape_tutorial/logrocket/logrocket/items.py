# Define here the models for your scraped items
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from dataclasses import dataclass

@dataclass
class LogrocketArticleItem:
    _id: str
    heading: str
    url: str
    author: str
    published_on: str
#end class