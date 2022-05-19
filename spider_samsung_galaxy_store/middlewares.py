# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from typing import List
from scrapy import signals, Spider
from scrapy.http import Request, Response

from samsung_galaxy_store import SamsungGalaxyStore, Category, AppSummary, App, Review

from .json_response import JsonResponse


class SamsungGalaxyStoreDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Request, spider: Spider):
        if request.url == "api://categories":
            categories: List[Category] = self.api.get_categories()
            return JsonResponse(url=request.url, jobject=categories, request=request)
        elif request.url.startswith("api://category_apps/"):
            category: Category = request.meta.get("category")
            start: int = request.meta.get("start")
            end: int = request.meta.get("end")
            apps: List[AppSummary] = list(
                self.api.get_category_apps(category, start, end)
            )
            return JsonResponse(url=request.url, jobject=apps, request=request)
        elif request.url.startswith("api://app/"):
            summary: AppSummary = request.meta.get("app")
            app: App = self.api.get_app_details(summary.guid)
            return JsonResponse(url=request.url, jobject=app, request=request)
        elif request.url.startswith("api://app_reviews/"):
            app: App = request.meta.get("app")
            start: int = request.meta.get("start")
            reviews: List[Review] = list(self.api.get_app_reviews_page(app.id, start))
            return JsonResponse(url=request.url, jobject=reviews, request=request)

        return None

    def process_response(self, request: Request, response: Response, spider: Spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request: Request, exception: Exception, spider: Spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider: Spider):
        spider.logger.info("Spider opened: %s" % spider.name)
        self.api: SamsungGalaxyStore = SamsungGalaxyStore()
