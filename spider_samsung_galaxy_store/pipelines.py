# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from hashlib import md5
from typing import Any, Dict
from scrapy import Spider
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.results import UpdateResult

from samsung_galaxy_store import Category, AppSummary, App, Review


class MongoPipeline:
    def __init__(self, uri: str, db: str) -> None:
        self.config_uri: str = uri
        self.config_db: str = db
        self.client: MongoClient = None
        self.db: Database = None

    @classmethod
    def from_crawler(cls, crawler) -> "MongoPipeline":
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
            _id: str = document.pop("id")
            self._upsert_document("categories", _id, document)
        elif isinstance(item, App):
            document: Dict[str, Any] = item.json()
            _id: str = document.pop("id")
            self._upsert_document("apps", _id, document)
        elif isinstance(item, AppSummary):
            document: Dict[str, Any] = item.json()
            _id: str = document.pop("id")

            # remove redundant category info from AppSummary
            # category_id is document reference to category
            document.pop("category_name")
            document.pop("category_class")

            self._upsert_document("apps", _id, document)
        elif isinstance(item, Review):
            document: Dict[str, Any] = item.json()

            app: App = item.app
            document.pop("app")
            document["app_id"] = app.id

            _id: str = md5(
                f"{app.id}:{item.user}:{item.user_id}:{item.stars}:{item.text}".encode(
                    "utf8"
                )
            ).hexdigest()
            self._upsert_document("reviews", _id, document)
        return item

    def _upsert_document(
        self, collection: str, _id: Any, document: Dict[str, Any]
    ) -> UpdateResult:
        filter: Dict[str, str] = {"_id": _id}
        update: Dict[str, Dict[str, Any]] = {
            "$set": self._flatten_document_for_update(document)
        }
        return self.db[collection].update_one(filter, update, upsert=True)

    def _flatten_document_for_update(self, document: Dict[str, Any]) -> Dict[str, Any]:
        flat: Dict[str, Any] = {}
        for key, value in document.items():
            if isinstance(value, dict):
                sub_flat: Dict[str, Any] = self._flatten_document_for_update(value)
                for sub_key, sub_value in sub_flat.items():
                    composite_key = f"{key}.{sub_key}"
                    flat[composite_key] = sub_value
            else:
                flat[key] = value
        return flat
