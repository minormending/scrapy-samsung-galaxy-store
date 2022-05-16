from ctypes import Union
from typing import Iterable, List
import scrapy
from scrapy.http import Request, Response

from samsung_galaxy_store import Category, AppSummary, App

from scrapy_samsung_galaxy_store.middlewares import JsonResponse


class SpiderSpider(scrapy.Spider):
    name = "galaxy-store"
    allowed_domains = ["galaxystore.samsung.com"]

    def start_requests(self) -> Request:
        yield Request(url="api://categories", callback=self.parse_categories)

    def parse_categories(self, response: JsonResponse) -> Iterable[Request | Category]:
        categories: List[Category] = response.json()
        for category in categories:
            yield category
            yield Request(url="api://category_apps", callback=self.parse_category_apps, meta={
                "category": category,
                "start": 1,
            })


    def parse_category_apps(self, response: JsonResponse):
        apps: List[AppSummary] = response.json()
        print(apps)