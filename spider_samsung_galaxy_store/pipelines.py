# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Any, Dict
from scrapy import Spider
from pymongo.mongo_client import MongoClient
from pymongo.database import Database

from samsung_galaxy_store import Category, Developer, AppSummary, App, Review


class MongoPipeline:
    def __init__(self, uri: str, db: str) -> None:
        self.config_uri: str = uri
        self.config_db: str = db
        self.client: MongoClient = None
        self.db: Database = None

    @classmethod
    def from_crawler(cls, crawler) -> 'MongoPipeline':
        return cls(
            uri=crawler.settings.get("MONGO_URI"),
            db=crawler.settings.get("MONGO_DB"),
        )

    def open_spider(self, spider: Spider):
        self.client: MongoClient = MongoClient(self.config_uri)
        self.db: Database = self.client[self.config_db]

    def close_spider(self, spider: Spider):
        self.client.close()

    def process_item(self, item: Any, spider: Spider):
        if isinstance(item, Category):
            document: Dict[str, Any] = item.json()
            id: str = document.pop("id")
            document["_id"] = id
            self.db['categories'].insert_one(document)
        elif isinstance(item, AppSummary):
            #document: Dict[str, Any] = item.json()
            #id: str = document.pop("id")
            #document["_id"] = id
            #self.db.categories.insert_one(document)
            pass
        return item
