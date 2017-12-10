from scrapy.spiders import Spider
from uf_scrapy.items import UF
import scrapy
import requests

class UFSpider(Spider):
    name = 'uf_spider'
    allowed_domains = ["si3.bcentral.cl"]
    url = 'http://si3.bcentral.cl/IndicadoresSiete/secure/Serie.aspx?gcode=UF&param=RABmAFYAWQB3AGYAaQBuAEkALQAzADUAbgBNAGgAaAAkADUAVwBQAC4AbQBYADAARwBOAGUAYwBjACMAQQBaAHAARgBhAGcAUABTAGUAYwBsAEMAMQA0AE0AawBLAF8AdQBDACQASABzAG0AXwA2AHQAawBvAFcAZwBKAEwAegBzAF8AbgBMAHIAYgBDAC4ARQA3AFUAVwB4AFIAWQBhAEEAOABkAHkAZwAxAEEARAA%3d'
    start_urls = [url]

    @staticmethod
    def crawl_table(response):
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

    def __init__(self, start_year='', end_year='',*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = []
        self.start_year = int(start_year)
        self.end_year = int(end_year)

    def parse(self, response):
        self.result = self.result + self.crawl_table(response)  # current year
        for year in range(self.start_year, self.end_year):
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'DrDwnFechas': str(year)},
                callback=self.parse_results,
            )

    def parse_results(self, response):
        self.result = self.result + self.crawl_table(response)

    def closed(self, _):
        self.result = sorted(self.result, key=lambda d: d['date'])
        url = "http://localhost:8000/uf/"
        response = requests.post(url, json=self.result, headers={'Content-Type': 'application/json'})
        if response.status_code != 201:
            self.logger.error("Couldn't store data")

