import scrapy


class ExpobankrsItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
