from scrapy.spiders import BaseSpider
from uf_scrapy.items import ScrapyUF

class AllUF(BaseSpider):
    name = "all"
    allowed_domains = ["si3.bcentral.cl"]
    start_urls = ['http://si3.bcentral.cl/IndicadoresSiete/secure/Serie.aspx?gcode=UF&param=RABmAFYAWQB3AGYAaQBuAEkALQAzADUAbgBNAGgAaAAkADUAVwBQAC4AbQBYADAARwBOAGUAYwBjACMAQQBaAHAARgBhAGcAUABTAGUAYwBsAEMAMQA0AE0AawBLAF8AdQBDACQASABzAG0AXwA2AHQAawBvAFcAZwBKAEwAegBzAF8AbgBMAHIAYgBDAC4ARQA3AFUAVwB4AFIAWQBhAEEAOABkAHkAZwAxAEEARAA%3d']

    def parse(self, response):
         table = response.xpath('//*[@id="gr"]/tbody')
         print(table)
         return ScrapyUF()
