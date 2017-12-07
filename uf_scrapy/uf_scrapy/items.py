from scrapy_djangoitem import DjangoItem
from uf_app.models import UF


class ScrapyUF(DjangoItem):
    django_model = UF
