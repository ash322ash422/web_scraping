import scrapy

#STEP1) ..\scrape_tutorial> mkdir quotes-scraper
#STEP2) ..\scrape_tutorial\quotes-scraper> scrapy runspider scraper.py
# OR    ..\scrape_tutorial\quotes-scraper> scrapy runspider scraper.py -o items.json -t json
#NOTE: Above command appends the results
class QuoteSpider(scrapy.Spider):
    name = 'quote-spider'
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):#override
        NEXT_SELECTOR = '.next a::attr("href")'

        for quote in response.css('.quote'):
            yield {
                'text':   quote.css('.text::text').extract_first(),
                'author': quote.css('.author::text').extract_first(),
                'auth_href': 'https://quotes.toscrape.com' + 
                          quote.css('.author + a::attr("href")').extract_first(),
                'tags':   quote.css('.tags > .tag::text').extract(),
            }
        
        """
        #Following works too. I am commenting it out to save time
        next_page = response.css(NEXT_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
            )
        """
#end class
"""
quotes.toscrape.com
<body>
...
    <div class="quote" itemscope itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>
        <span>by <small class="author" itemprop="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="change,deep-thoughts,thinking,world" /    > 
            <a class="tag" href="/tag/change/page/1/">change</a>
            <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
            <a class="tag" href="/tag/thinking/page/1/">thinking</a>
            <a class="tag" href="/tag/world/page/1/">world</a>
        </div>
    </div>

    <div class="quote" itemscope itemtype="http://schema.org/CreativeWork">
        <span class="text" itemprop="text">“It is our choices, Harry, that show what we truly are, far more than our abilities.”</span>
        <span>by <small class="author" itemprop="author">J.K. Rowling</small>
        <a href="/author/J-K-Rowling">(about)</a>
        </span>
        <div class="tags">
            Tags:
            <meta class="keywords" itemprop="keywords" content="abilities,choices" /    > 
            <a class="tag" href="/tag/abilities/page/1/">abilities</a>
            <a class="tag" href="/tag/choices/page/1/">choices</a>
        </div>
    </div>
    ...
    <nav>
        <ul class="pager">
            <li class="next">
                <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
            </li>
        </ul>
    </nav>
...    
</body>    
"""

"""
....
2024-06-15 11:43:02 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://quotes.toscrape.com> (referer: None)
2024-06-15 11:43:03 [scrapy.core.scraper] DEBUG: Scraped from <200 https://quotes.toscrape.com>
{'text': '“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”', 'author': 'Albert Einstein', 'about': 'https://quotes.toscrape.com/author/Albert-Einstein', 'tags': ['change', 'deep-thoughts', 'thinking', 'world']}
2024-06-15 11:43:03 [scrapy.core.scraper] DEBUG: Scraped from <200 https://quotes.toscrape.com>
{'text': '“It is our choices, Harry, that show what we truly are, far more than our abilities.”', 'author': 'J.K. Rowling', 'about': 'https://quotes.toscrape.com/author/J-K-Rowling', 'tags': ['abilities', 'choices']}
2024-06-15 11:43:03 [scrapy.core.scraper] DEBUG: Scraped from <200 https://quotes.toscrape.com>
....
2024-06-15 11:43:03 [scrapy.core.scraper] DEBUG: Scraped from <200 https://quotes.toscrape.com>
{'text': '“A day without sunshine is like, you know, night.”', 'author': 'Steve Martin', 'about': 'https://quotes.toscrape.com/author/Steve-Martin', 'tags': ['humor', 'obvious', 'simile']}
2024-06-15 11:43:03 [scrapy.core.engine] INFO: Closing spider (finished)
2024-06-15 11:43:03 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 220,
 'downloader/request_count': 1,
 ...
"""
