from scrapy import Spider
from scrapy.selector import Selector
from stack.items import StackItem

#STEP 1)..\scrape_tutorial>scrapy startproject stack
#Then add necessary code in settings.py, items.py, pipelines.py, stack_spider.py
#STEP 2)..\scrape_tutorial\stack> scrapy crawl stack
# or    ..\scrape_tutorial\stack> scrapy crawl stack -o items.json -t json

#NOTE: To launch shell use following command:
# scrapy shell "http://stackoverflow.com/questions?pagesize=50&sort=newest"

class StackSpider(Spider):
    name = "stack" #defines the name of the Spider.
    #Following contains the base-URLs for the allowed domains for the spider to crawl
    allowed_domains = ["stackoverflow.com"]
    #following is list of URLs for the spider to start crawling from. All subsequent 
    # URLs will start from the data that the spider downloads from the URLS in start_urls
    start_urls = ["http://stackoverflow.com/questions?pagesize=50&sort=newest",]

    def STYLE1_parse(self, response):#works
        #Following returns list. See below for a sample of HTML
        questions_title = response.xpath('//a[@class="s-link"]/text()').getall() 
        questions_href  = response.xpath('//a[@class="s-link"]/@href').getall()
        
        for i in range(len(questions_title)):
            item = StackItem()
            item['title'] = questions_title[i]
            item['url']   = 'stackoverflow.com' + questions_href[i]
            yield item
        #end for
        
    #end def
    
    def parse(self, response): #override
        #Following returns list. See below for a sample of HTML
        questions = response.xpath('//a[@class="s-link"]')
        for q in questions:# NOTE: q is of type <class 'scrapy.selector.unified.Selector'>
            #output of print(q)= <a href="/questions/78628224/what-could-be-blocking-npx" 
            #  class="s-link">what could be blocking 'npx create-react-app &lt;app name&gt;' 
            #  from working from the error</a>
            item = StackItem()
            item['title'] = q.xpath('text()').get()
            item['url'] = 'stackoverflow.com' + q.attrib['href']
            yield item
        #end for
    #end def
#end class
"""
....
<a href="/questions/78627223/align-y-axis-start-for-subplots-in-pyqtgraph" 
   class="s-link">Align Y axis start for subplots in pyqtgraph</a>
....
"""