from typing import Iterable, List
from scrapy import Spider
from scrapy.http import Request
from samsung_galaxy_store import Category, AppSummary, App, Review

from spider_samsung_galaxy_store.middlewares import JsonResponse
from spider_samsung_galaxy_store.router import Router


class SpiderSpider(Spider):
    name = "galaxy-store"
    CATEGORY_APPS_PAGE_SIZE = 500
    APP_REVIEWS_PAGE_SIZE = 15

    def start_requests(self) -> Request:
        yield Request(url=Router.build_categories_uri(), callback=self.parse_categories)

    def parse_categories(self, response: JsonResponse) -> Iterable[Request | Category]:
        categories: List[Category] = response.json()
        for category in categories:
            yield category
            yield Request(
                url=Router.build_category_apps_uri(category, start=1),
                meta={
                    "category": category,
                    "start": 1,
                    "end": self.CATEGORY_APPS_PAGE_SIZE,
                },
                callback=self.parse_category_apps,
            )

    def parse_category_apps(self, response: JsonResponse) -> Iterable[Request | App]:
        request: Request = response.request
        category: Category = request.meta.get("category")
        apps: List[AppSummary] = response.json()
        for app in apps:
            yield app
            yield Request(
                url=Router.build_app_details_uri(app),
                meta={
                    "category": category,
                    "app": app,
                },
                callback=self.parse_app_details,
            )

        if len(apps) == self.CATEGORY_APPS_PAGE_SIZE:
            start: int = request.meta.get("start") + self.CATEGORY_APPS_PAGE_SIZE
            yield Request(
                url=Router.build_category_apps_uri(category, start),
                meta={
                    "category": category,
                    "start": start,
                    "end": self.CATEGORY_APPS_PAGE_SIZE,
                },
                callback=self.parse_category_apps,
            )

    def parse_app_details(self, response: JsonResponse) -> Iterable[App]:
        app: App = response.json()
        yield app

        if app.review_count:
            yield Request(
                url=Router.build_app_reviews_uri(app, start=1),
                meta={"app": app, "start": 1},
                callback=self.parse_app_reviews,
            )

    def parse_app_reviews(self, response: JsonResponse):
        request: Request = response.request
        app: App = request.meta.get("app")
        reviews: List[Review] = response.json()
        for review in reviews:
            review.app = app
            yield review

        if len(reviews) == self.APP_REVIEWS_PAGE_SIZE:
            start: int = request.meta.get("start") + self.APP_REVIEWS_PAGE_SIZE
            yield Request(
                url=Router.build_app_reviews_uri(app, start),
                meta={"app": app, "start": start},
                callback=self.parse_app_reviews,
            )
