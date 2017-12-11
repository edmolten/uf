from unittest import TestCase
from django.test import Client
import json


class ApiTest(TestCase):
    def test_price(self):
        url = "/uf/price/"
        client = Client()
        cases = [('2013-04-02', '100', '2287085.00'),
                 ('1987-03-30', '77', '267067.57'),
                 ('1997-01-31', '7', '93334.85'),
                 ('2005-07-05', '123', '2152252.77'),
                 ('2017-12-31', '2', '53596.28')
                 ]
        for date, value, expected in cases:
            response = client.get(url, {'date': date, 'value': value})
            content = float(response.content.decode('utf-8'))
            self.assertEqual("{:.2f}".format(content), expected)

    def test_list_until_2017_12_31(self):
        url = "/uf/list/"
        client = Client()
        response = client.get(url)
        all_data = response.json()
        all_data = sorted(all_data, key=lambda d: d['date'])
        data = []
        for uf in all_data:
            if uf["date"] == "2018-01-01":
                break
            data.append(uf)
        with open('data.json', 'w') as data_file:
            json.dump(data, data_file)
        test_data = json.load(open('data.json'))
        equal = True
        for i in range(len(data)):
            if data[i] != test_data[i]:
                equal = False
        self.assertTrue(equal)

    def test_imposible_date(self):
        url = "/uf/price/"
        client = Client()
        cases = ['2013-04-33',
                 '1987-03-32',
                 '1997-02-30',
                 '2005-07-05'
                 ]
        for date in cases:
            response = client.get(url, {'date': date, 'value': '1'})
            self.assertTrue(response.status_code, 404)

    def test_not_available_date(self):
        url = "/uf/price/"
        client = Client()
        cases = ['1977-04-01',
                 '1977-03-31',
                 '2018-02-30',
                 '2666-07-05'
                 ]
        for date in cases:
            response = client.get(url, {'date': date, 'value': '1'})
            self.assertTrue(response.status_code, 404)