# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from typing import List
from scrapy import signals, Spider
from scrapy.http import Request, Response

from samsung_galaxy_store import SamsungGalaxyStore, Category, AppSummary, App, Review

from .json_response import JsonResponse
from .router import Router


class ApiDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        middleware: ApiDownloaderMiddleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def process_request(self, request: Request, spider: Spider):
        if Router.is_categories_uri(request.url):
            categories: List[Category] = self.api.get_categories()
            return JsonResponse(url=request.url, jobject=categories, request=request)
        elif Router.is_category_apps_uri(request.url):
            category: Category = request.meta.get("category")
            start: int = request.meta.get("start")
            end: int = request.meta.get("end")
            apps: List[AppSummary] = list(
                self.api.get_category_apps(category, start, end)
            )
            return JsonResponse(url=request.url, jobject=apps, request=request)
        elif Router.is_app_details_uri(request.url):
            summary: AppSummary = request.meta.get("app")
            app: App = self.api.get_app_details(summary.guid)
            return JsonResponse(url=request.url, jobject=app, request=request)
        elif Router.is_app_reviews_uri(request.url):
            app: App = request.meta.get("app")
            start: int = request.meta.get("start")
            reviews: List[Review] = list(self.api.get_app_reviews_page(app.id, start))
            return JsonResponse(url=request.url, jobject=reviews, request=request)

        return None

    def process_response(self, request: Request, response: Response, spider: Spider):
        return response

    def process_exception(self, request: Request, exception: Exception, spider: Spider):
        pass

    def spider_opened(self, spider: Spider):
        spider.logger.info("Spider opened: %s" % spider.name)
        self.api: SamsungGalaxyStore = SamsungGalaxyStore()
