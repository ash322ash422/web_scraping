import scrapy
from ..items import LogrocketArticleItem
#STEP 1) ..\scrape_tutorial>scrapy startproject logrocket
#STEP 2) scrapy genspider <spider_name> <url_to_be_scraped>
# ..\scrape_tutorial\logrocket> scrapy genspider feature_article blog.logrocket.com
#Then add necessary code in dir ../spiders/feature_article.py, settings.py, items.py and pipelines.py
#STEP 3)..\scrape_tutorial\logrocket> scrapy crawl feature_article
# or    ..\scrape_tutorial\logrocket> scrapy crawl feature_article -o items.json -t json
#NOTE: Above command appends the results
class FeatureArticleSpider(scrapy.Spider):
    name = 'feature_article'#defines the spider. Must be unique within the project
    allowed_domains = ['blog.logrocket.com']# list of domains that we are allowed to crawl
    start_urls = ['https://blog.logrocket.com'] #list of urls where we begin the crawl

    #NOTE: see screen shot image of html in PDF file
    #Following is called to handle the response of the request. It generally parses
    # the response, extracts the data, and yields it in the form of dict/object
    def parse(self, response):#override
        
        feature_articles = response.css(".post-card")
        #print("len(feature_articles)=",len(feature_articles))
        for article in feature_articles:
            article_obj = LogrocketArticleItem(
                _id = article.css("::attr('id')").extract_first(),
                heading = article.css("h4.post-card-title::text").extract_first(),
                url = article.css("a::attr(href)").extract_first(),
                author = article.css(".post-card-author-name::text").extract_first(),
                published_on = article.css("div:nth-child(2) > div::text").extract_first(),
            )
            yield article_obj
        #end for
        
    #end def
    
#end class
            
            
            