# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Any
from itemadapter import ItemAdapter
from scrapy import Spider
from pymongo.mongo_client import MongoClient
from pymongo.database import Database


class MongoDBPipeline:
    def __init__(self, uri: str, db: str) -> None:
        self.config_uri: str = uri
        self.config_db: str = db
        self.client: MongoClient = None
        self.db: Database = None

    @classmethod
    def from_crawler(cls, crawler) -> 'MongoDBPipeline':
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
        return item
