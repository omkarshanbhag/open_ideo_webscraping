import scrapy
from scrapy import Selector
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
import urllib

def to_write(uni_str):
    return urllib.unquote(uni_str.encode('utf8')).decode('utf8')

class OpenSpider(Spider):
    name = "OpenIDEO"
    allowed_domains = ["openideo.com"]
    start_urls = ["https://challenges.openideo.com/challenge"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//h2")
        url_list = []
        for title in titles:
            title = titles.select("a/@href").extract()
        x = 0
        while x < len(title):
            title[x] = 'https://challenges.openideo.com' + title[x]
            x += 1
        for url in title:
            #submitted_to = url
            yield scrapy.Request(url=url, callback=self.page_finder)

    def page_finder(self,response):
        page_inspiration = response.css('div.inspiration a::attr(href)').extract()
        #goes to the research submission page instead of the page at the beginning of the url
        for p in page_inspiration:
            if not p == '#' and not p == []:
                yield scrapy.Request(url='https://challenges.openideo.com' + p, callback=self.traverse)

        page_concepting = response.css('div.concepting a::attr(href)').extract()
        #goes to concepting submission page instead of the page at the beginning of the url
        for p in page_concepting:
            if not p == '#' and not p == []:
                yield scrapy.Request(url='https://challenges.openideo.com' + p, callback=self.traverse)

    def traverse(self,response):
        page_num = int(response.css("span.js-page-count::text").extract_first())
		# page_num = 1

        for i in range(1,page_num+1):
            url = response.url + "?page=" + str(i)
            yield scrapy.Request(url=url, callback=self.page)

    def page(self,response):
        rows = response.css('div.col-keep-distance')
        for row in rows:
            articles = row.css('article')
            for article in articles:
                contribution_page_url = article.css('h1.listing-title a::attr(href)').extract_first()
                contribution_page = response.urljoin(contribution_page_url)
                yield scrapy.Request(url=contribution_page, callback=self.contribution)

    def contribution(self, response):
        author_url = response.css('div.details h1.secondary-text a::attr(href)').extract_first()
        author_page = response.urljoin(author_url)
		# yield {
		# 	"contribution":response.css('h1.headline-text::text').extract_first(),
		# }
        yield scrapy.Request(url=author_page, callback=self.author)

    def author(self, response):
        #print(response.css('h1.headline-text::text').extract_first().strip())
        #print(response.css('div.collapsed-section//span[@id='secondary-text::text').extract().strip())s

        #Get person's Geolocation if listed
        """"if not response.css('p.geolocation::text').extract_first():
            geo = "Not Specified"
        else:
            geo = response.css('p.geolocation::text').extract_first().strip()"""

        #Get person's Job title or occupation if listed
        if not response.css('p.occupation::text').extract_first():
            job = "Not Specified"
        else:
            job = response.css('p.occupation::text').extract_first().strip()

        #Get person's company if listed
        if not response.css('p.company::text').extract_first():
            company = "Not Specified"
        else:
            company = response.css('p.company::text').extract_first().strip()

        author = response.css('h1.headline-text::text').extract_first().strip()

        yield {
            "author": author,
            "geolocation": to_write(response.css('p.geolocation::text').extract_first().strip()),
            "occupation": job,
            "company": company,

            #"submission": submitted_to,
			# "author": response.css('h1.headline-text::text').extract_first(),
			# "geolocation": response.css('p.geolocation::text').extract_first(),
        }
