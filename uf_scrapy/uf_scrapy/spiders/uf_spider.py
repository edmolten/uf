from scrapy.spiders import Spider
from scrapy import FormRequest
import json
import scrapy
import datetime

class UFSpider(Spider):
    name = 'bc_spider'
    allowed_domains = ["si3.bcentral.cl"]
    url = 'http://si3.bcentral.cl/IndicadoresSiete/secure/Serie.aspx?gcode=UF&param=RABmAFYAWQB3AGYAaQBuAEkALQAzADUAbgBNAGgAaAAkADUAVwBQAC4AbQBYADAARwBOAGUAYwBjACMAQQBaAHAARgBhAGcAUABTAGUAYwBsAEMAMQA0AE0AawBLAF8AdQBDACQASABzAG0AXwA2AHQAawBvAFcAZwBKAEwAegBzAF8AbgBMAHIAYgBDAC4ARQA3AFUAVwB4AFIAWQBhAEEAOABkAHkAZwAxAEEARAA%3d'
    start_urls = [url]
    result = []

    def parse(self, response): # TODO not writing in file, try print array
        for year in range(1977, datetime.datetime.now().year):
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'DrDwnFechas': str(year)},
                callback=self.parse_results,
            )
        f = open("result", "w")
        for uf in UFSpider.result:
            f.write(str(uf) + '\n')
        f.close()

    def prepend_zero(self, x):
        if x < 10:
            return "0" + str(x)
        return str(x)

    def crawl_table(self, response):
        table = response.xpath('//table[@id="gr"]//tr')
        year = response.xpath('//*[@id="lblAnioValor"]/text()').extract_first()
        d = 1
        # f = open("result", "a")
        result = []
        for row in table[1:]:
            for m in range(2, 14):
                value = row.xpath('.//td[{}]/span/text()'.format(m)).extract_first()
                if (value):
                    date = "{}-{}-{}".format(year, self.prepend_zero(m - 1), self.prepend_zero(d))
                    uf = {'date': date, 'value': value}
                    result.append(uf)
                    #     f.write(str({'date': date, 'value': value})+'\n')
            d += 1
        return result#.sort()

    def parse_results(self, response):
        UFSpider.result = UFSpider.result + self.crawl_table(response)
