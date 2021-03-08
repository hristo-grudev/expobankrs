import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import ExpobankrsItem
from itemloaders.processors import TakeFirst


class ExpobankrsSpider(scrapy.Spider):
	name = 'expobankrs'
	start_urls = ['https://www.expobank.rs/index.php/ru/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="wrap t3-sl t3-sl-1"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="article-title"]//text()[normalize-space()]').get()
		description = response.xpath('//section[@class="article-content clearfix"]//text()[normalize-space()]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=ExpobankrsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
