import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['galaxystore.samsung.com']
    start_urls = ['http://galaxystore.samsung.com/']

    def parse(self, response):
        pass
