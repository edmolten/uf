import scrapy


class ScrapyUF(scrapy.Item):
    date = scrapy.Field()
    value = scrapy.Field()
