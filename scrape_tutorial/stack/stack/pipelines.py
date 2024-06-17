# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem

settings = get_project_settings() # a dictionary

class MongoDBPipeline(object):

    def __init__(self):
        mongo_client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = mongo_client[settings['MONGODB_DB']]
        
        self.collection = db[settings['MONGODB_COLLECTION']]
        qry = {} #an empty query b/c we want total count. O/w, queries can be specified here
        if self.collection.count_documents(qry) != 0: # if docs are in collection
            self.collection.drop() #then drop collection & start afresh
    #end def
    
    def process_item(self, item, spider):#override
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        #end for
        
        if valid:
            self.collection.insert_one(dict(item))
            
        return item
    #end def
    
#end class
"""
..\scrape_tutorial\stack\stack> cat .\items.py
from scrapy.item import Item, Field

class StackItem(Item):
    title = Field()
    url = Field()
#end class
..\scrape_tutorial\stack\stack>
"""       