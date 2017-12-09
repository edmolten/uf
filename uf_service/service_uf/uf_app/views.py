from django.http import Http404

from uf_app.models import UF
from uf_app.serializers import UFSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.db import transaction
import datetime
from scrapy.crawler import CrawlerProcess
from uf_scrapy.uf_scrapy.spiders.uf_spider import UFSpider
from scrapy.utils.project import get_project_settings


class UFList(APIView):

    @staticmethod
    def missing_data(data):
        last = data.last().date
        next = last + datetime.timedelta(days=1)
        return UFtoCLP.available(next)

    def get(self, request):
        data = UF.objects.all()
        if len(data) == 0:
            UFSpider.populate()
        elif UFList.missing_data(data):
            last_year = data.last().date.year
            UFSpider.crawl_until_available(last_year)
        data = UF.objects.all()
        serializer = UFSerializer(data, many=True)
        return Response(serializer.data)


class UFCreateMany(APIView):
    def post(self, request):
        data = UF.filter(request.data)
        serializer = UFSerializer(data=data, many=True)
        if serializer.is_valid():
            self.save_all(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def save_all(self, data):
        for uf in data:
            entry = UF(date=uf['date'], value=uf['value'])
            entry.save()


class UFtoCLP(APIView):
    def get(self, request):
        date = request.query_params['date']
        amount = int(request.query_params['value'])
        uf = UF.get(date)
        if uf:
            clp = uf.get_price(amount)
            return Response(float(clp))
        else:
            last_uf = UF.objects.last()
            if last_uf:
                UFSpider.crawl_until_available(last_uf.date.year)
            else:
                UFSpider.populate()
            uf = UF.get(date)
            if uf:
                clp = uf.get_price(amount)
                return Response(float(clp))
        raise Http404

