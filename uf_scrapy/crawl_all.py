from scrapy.crawler import CrawlerProcess
from uf_scrapy.spiders.uf_spider import UFSpider
from scrapy.utils.project import get_project_settings
import datetime

process = CrawlerProcess(get_project_settings())
process.crawl(UFSpider, start_year=1977, end_year=datetime.datetime.now().year)
process.start()
