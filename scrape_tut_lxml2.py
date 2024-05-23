import asyncio
import json
from lxml import etree
from httpx import AsyncClient, Response
from typing import List, Dict

def parse_products(response: Response) -> List[Dict]:
    """parse products from HTML"""
    # create a lxml selector
    selector = etree.fromstring(response.text)
    data = []
    for product in selector.xpath("//div[@class='row product']"):
        name = product.xpath(".//div[contains(@class, description)]/h3/a/text()").get()
        link = product.xpath(".//div[contains(@class, description)]/h3/a/@href").get()
        product_id = link.split("/product/")[-1]
        price = float(product.xpath(".//div[@class='price']/text()").get())
        data.append({
            "product_id": int(product_id),
            "name": name,
            "link": link,
            "price": price
        })
    return data


# initializing a async httpx client
client = AsyncClient(
    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }
)

def parse_products(response: Response) -> List[Dict]:
    """parse products from HTML"""
    # create a lxml selector
    parser = etree.HTMLParser()
    selector = etree.fromstring(response.text, parser)
    data = []
    for product in selector.xpath("//div[@class='row product']"):
        name = product.xpath(".//div[contains(@class, description)]/h3/a/text()")[0]
        link = product.xpath(".//div[contains(@class, description)]/h3/a/@href")[0]
        price = float(product.xpath(".//div[@class='price']/text()")[0])
        data.append({
            "name": name,
            "link": link,
            "price": price
        })
    return data


async def scrape_products(url: str) -> List[Dict]:
    """scrape product pages"""
    # scrape the first product page first
    first_page = await client.get(url)
    products_data = parse_products(first_page)
    # add the remaining product pages to a scraping list
    other_pages = [
        client.get(url + f"?page={page_number}")
        # the maximum available pages are 5
        for page_number in range(2, 5 + 1)
    ]
    for response in asyncio.as_completed(other_pages):
        response = await response
        data = parse_products(response)
        # extend the first page data with new ones
        products_data.extend(data)
    print(f"scraped {len(products_data)} products")
    return products_data

async def run():
    data = await scrape_products(
        url="https://web-scraping.dev/products"
    )
    # print the results in JSON format
    print(json.dumps(data, indent=2))

if __name__=="__main__":
    asyncio.run(run())

"""
scraped 25 products
[
  {
    "name": "Box of Chocolate Candy",
    "link": "https://web-scraping.dev/product/1",
    "price": 24.99
  },
  {
    "name": "Dark Red Energy Potion",
    "link": "https://web-scraping.dev/product/2",
    "price": 4.99
  },
 ...
  {
    "name": "Box of Chocolate Candy",
    "link": "https://web-scraping.dev/product/25",
    "price": 24.99
  }
]    
    
"""