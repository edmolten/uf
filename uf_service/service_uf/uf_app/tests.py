from unittest import TestCase
from django.test import Client


class ApiTest(TestCase):

    def test_price(self):
        url = "/uf/price/"
        client = Client()
        cases = [('2013-04-02', '100', '2287085.00'),
                 ('1987-03-30', '77', '267067.57'),
                 ('1997-01-31', '7', '93334.85'),
                 ('2005-07-05', '123', '2152252.77')
                 ]
        for date, value, expected in cases:
            response = client.get(url, {'date': date, 'value': value})
            content = float(response.content.decode('utf-8'))
            self.assertEqual("{:.2f}".format(content), expected)