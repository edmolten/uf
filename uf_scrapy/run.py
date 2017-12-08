from scrapy.crawler import CrawlerProcess
from uf_scrapy.spiders.uf_spider import UFSpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(UFSpider)
process.start()
