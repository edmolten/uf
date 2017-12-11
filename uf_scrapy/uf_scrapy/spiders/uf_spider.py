from scrapy.spiders import Spider
from uf_scrapy.items import UF
from constants import *
from scrapy import FormRequest
from datetime import datetime
import requests
import json


class UFSpider(Spider):
    name = SPIDER_NAME
    allowed_domains = [BC_HOST]
    url = UF_URL
    start_urls = [url]

    @staticmethod
    def crawl_table(response):
        rows = response.xpath(ALL_ROWS_XPATH)
        year = response.xpath(YEAR_XPATH).extract_first()
        day = 1
        result = []
        for row in rows[1:]:
            for month in range(2, 14):
                value = row.xpath(VALUE_FORMATED_XPATH.format(month)).extract_first()
                if value:
                    result.append(UF.create(year, month - 1, day, value))
            day += 1
        return result

    def __init__(self, start_year='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = []
        self.start_year = int(start_year)

    def parse(self, response):
        self.result = self.result + self.crawl_table(response)  # current year
        today = datetime.today()
        if today.month == 12 and today.day > 9:
            end_year = today.year + 1
        else:
            end_year = today.year
        for year in range(self.start_year, end_year):
            yield FormRequest.from_response(
                response,
                formdata={DROPDOWN_YEAR_INPUT: str(year)},
                callback=self.parse_results,
            )

    def parse_results(self, response):
        self.result = self.result + self.crawl_table(response)

    def closed(self, _):
        self.result = sorted(self.result, key=lambda d: d['date'])
        with open('test.json', 'w') as data_file:
            json.dump(self.result, data_file)
        response = requests.post(API_CREATE_MANY_URL,
                                 json=self.result,
                                 headers={'Content-Type': 'application/json'})
        if response.status_code != 201:
            self.logger.error("Couldn't store data")

