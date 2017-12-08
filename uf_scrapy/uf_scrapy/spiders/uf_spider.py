from scrapy.spiders import Spider
from uf_scrapy.items import UF
import scrapy
import datetime
import requests

class UFSpider(Spider):
    name = 'bc_spider'
    allowed_domains = ["si3.bcentral.cl"]
    url = 'http://si3.bcentral.cl/IndicadoresSiete/secure/Serie.aspx?gcode=UF&param=RABmAFYAWQB3AGYAaQBuAEkALQAzADUAbgBNAGgAaAAkADUAVwBQAC4AbQBYADAARwBOAGUAYwBjACMAQQBaAHAARgBhAGcAUABTAGUAYwBsAEMAMQA0AE0AawBLAF8AdQBDACQASABzAG0AXwA2AHQAawBvAFcAZwBKAEwAegBzAF8AbgBMAHIAYgBDAC4ARQA3AFUAVwB4AFIAWQBhAEEAOABkAHkAZwAxAEEARAA%3d'
    start_urls = [url]
    result = [] #TODO self

    def parse(self, response):
        UFSpider.result = UFSpider.result + self.crawl_table(response) # current year
        for year in range(1977, datetime.datetime.now().year):
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'DrDwnFechas': str(year)},
                callback=self.parse_results,
            )

    def prepend_zero(self, x):
        if x < 10:
            return "0" + str(x)
        return str(x)

    def crawl_table(self, response):
        table = response.xpath('//table[@id="gr"]//tr')
        year = response.xpath('//*[@id="lblAnioValor"]/text()').extract_first()
        day = 1
        result = []
        for row in table[1:]:
            for month in range(2, 14):
                value = row.xpath('.//td[{}]/span/text()'.format(month)).extract_first()
                if value:
                    result.append(UF.create(year, month - 1, day, value))
            day += 1
        return result

    def parse_results(self, response):
        UFSpider.result = UFSpider.result + self.crawl_table(response)

    def closed(self, cause):

        UFSpider.result = sorted(UFSpider.result, key=lambda d: d['date'])
        url = "http://localhost:8000/uf/"
        response = requests.post(url, json=UFSpider.result, headers={'Content-Type':'application/json'})
        if response.status_code != 201:
            self.logger.error("Couldn't store data")

