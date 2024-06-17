# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from scrapy.utils.project import get_project_settings
from .items import (
    LogrocketArticleItem
)
from dataclasses import asdict

settings = get_project_settings() # a dictionary

class MongoDBPipeline:
    def __init__(self):#override
        mongo_client = pymongo.MongoClient(
            settings.get('MONGO_HOST'),
            settings.get('MONGO_PORT')
        )
        db = mongo_client[settings.get('MONGO_DB_NAME')]# = "LOGROCKET"
        #if coll does not exist, then following would create
        self.collection = db[settings['MONGO_COLLECTION_NAME']]#="featured_articles"
        
        #Following works too
        """
        CONNECTION_STRING = 'mongodb://localhost:27017'
        mongo_client = pymongo.MongoClient(CONNECTION_STRING)
        db = mongo_client[settings.get('MONGO_DB_NAME')]
        collection_name = settings['MONGO_COLLECTION_NAME']
         
        if collection_name not in db.list_collection_names():
            self.collection = db.create_collection(collection_name)
        else:
            self.collection = db.get_collection(collection_name)
        """
           
    def process_item(self, item, spider): #override
        
        if isinstance(item, LogrocketArticleItem): # article item
            query = {"_id": item._id} # query item that would be updated
            new_updated_values = { "$set": asdict(item) }
            self.collection.update_one(query, new_updated_values , upsert = True)
        #end if
        return item
    
    #end def
"""
..\scrape_tutorial\logrocket\logrocket> cat .\items.py
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
..\scrape_tutorial\logrocket\logrocket> 
"""