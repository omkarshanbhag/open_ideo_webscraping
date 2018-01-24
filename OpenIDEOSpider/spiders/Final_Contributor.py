import scrapy
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.crawler import CrawlerProcess

class OpenSpider(BaseSpider):
    name = "OpenIDEO"
    allowed_domains = ["openideo.com"]
    start_urls = ["https://challenges.openideo.com/challenge"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//h2")
        url_list = []
        url_dict = {}
        for title in titles:
            title = titles.select("a/@href").extract()
        x = 0
        while x < len(title):
            title[x] = 'https://challenges.openideo.com' + title[x]
            x += 1
        url_dict['a'] = titles
        return url_dict

"""class ContributorsSpider(scrapy.Spider):
    name = "contributors"

    def start_requests(self):
        process = CrawlerProcess()
        y = process.crawl(OpenSpider)
        process.start()

        return y[a]"""
