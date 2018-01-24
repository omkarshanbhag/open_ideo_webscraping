import scrapy

class ContributorsSpider(scrapy.Spider):
	name = "contributors"

	def start_requests(self):
		urls = [
		'https://challenges.openideo.com/challenge/combatzikafuturethreats/research',
		'https://challenges.openideo.com/challenge/future-of-highered/research',
		'https://challenges.openideo.com/challenge/financial-longevity/research']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.traverse)

	def traverse(self,response):
		page_num = int(response.css("span.js-page-count::text").extract_first())
		# page_num = 1

		for i in range(1,page_num+1):
			url = response.url + "?page=" + str(i)
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self,response):
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
		yield {
			"author": response.css('h1.headline-text::text').extract_first().strip(),
			"geolocation": response.css('p.geolocation::text').extract_first().strip(),
			# "author": response.css('h1.headline-text::text').extract_first(),
			# "geolocation": response.css('p.geolocation::text').extract_first(),

		}
