import scrapy

from scrapy.loader import ItemLoader
from ..items import BancaditaliaItem
from itemloaders.processors import TakeFirst


class BancaditaliaSpider(scrapy.Spider):
	name = 'bancaditalia'
	start_urls = ['https://www.bancaditalia.it/media/notizie/index.html']


	def parse(self, response):
		year_links = response.xpath('//div[@class="side-nav"]/ul/li[2]/ul/li/a/@href').getall()
		for link in year_links:
			yield response.follow(link, self.parse_year)

	def parse_year(self, response):
		post_links = response.xpath('//ol[@class="listacom"]/li/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="meta-info"]/p/span/text()').get()

		item = ItemLoader(item=BancaditaliaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
