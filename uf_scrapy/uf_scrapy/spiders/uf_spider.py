from scrapy.spiders import Spider
from scrapy import FormRequest
import json
import scrapy


class UFSpider(Spider):
    name = 'bc_spider'
    allowed_domains = ["si3.bcentral.cl"]
    url = 'http://si3.bcentral.cl/IndicadoresSiete/secure/Serie.aspx?gcode=UF&param=RABmAFYAWQB3AGYAaQBuAEkALQAzADUAbgBNAGgAaAAkADUAVwBQAC4AbQBYADAARwBOAGUAYwBjACMAQQBaAHAARgBhAGcAUABTAGUAYwBsAEMAMQA0AE0AawBLAF8AdQBDACQASABzAG0AXwA2AHQAawBvAFcAZwBKAEwAegBzAF8AbgBMAHIAYgBDAC4ARQA3AFUAVwB4AFIAWQBhAEEAOABkAHkAZwAxAEEARAA%3d'
    start_urls = [url]

    def parse(self, response):

        yield scrapy.FormRequest.from_response(
            response,
            formdata={'DrDwnFechas': '2000'},
            callback=self.parse_results,
        )

    def prepend_zero(self, x):
        if x < 10:
            return "0" + str(x)
        return str(x)

    def parse_results(self, response):
        table = response.xpath('//table[@id="gr"]//tr')
        d = 1
        f = open("result", "w")
        for row in table[1:]:
            for m in range(2, 14):
                value = row.xpath('.//td[{}]/span/text()'.format(m)).extract_first()
                if(value):
                    date = "{}-{}-{}".format(2000, self.prepend_zero(m-1), self.prepend_zero(d))
                    f.write(str({'date': date, 'value': value}))
            d += 1
        f.close()
