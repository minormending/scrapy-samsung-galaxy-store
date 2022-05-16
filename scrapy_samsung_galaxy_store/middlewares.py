# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json
from typing import List
from scrapy import signals
from scrapy.http import Request, Response, TextResponse

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


from samsung_galaxy_store import SamsungGalaxyStore, Category, AppSummary, App


class JsonResponse(Response):
    def __init__(
        self,
        url,
        jobject,
        status=200,
        headers=None,
        body=b"",
        flags=None,
        request=None,
        certificate=None,
        ip_address=None,
        protocol=None,
    ):
        super().__init__(
            url,
            status,
            headers,
            body,
            flags,
            request,
            certificate,
            ip_address,
            protocol,
        )
        self.jobject = jobject
        self.jtext = None

    @property
    def text(self):
        if self.jtext is None:
            self.jtext: str = json.dumps(self.jobject)
        return self.jtext

    def json(self):
        return self.jobject


class SamsungGalaxyStoreDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Request, spider):
        print("=" * 10, request.url)
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
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
        self.api: SamsungGalaxyStore = SamsungGalaxyStore()
