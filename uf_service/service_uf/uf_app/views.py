from uf_app.models import UF
from uf_app.serializers import UFSerializer
from django.http import Http404
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
        today = datetime.datetime.today()
        data = UF.objects.all()
        if len(data) == 0:
            UFSpider.run(1977, today.year)
        elif UFList.missing_data(data):
            last_year = data.last().date.year
            if today.month == 12 and today.day > 10:
                UFSpider.run(last_year, today.year+1)
            else:
                UFSpider.run(last_year, today.year)
        data = UF.objects.all()
        serializer = UFSerializer(data, many=True)
        return Response(serializer.data)

class UFCreateMany(APIView):
    def post(self, request):
        data = self.filter(request.data)
        serializer = UFSerializer(data=data, many=True)
        if serializer.is_valid():
            self.save_all(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def filter(self, data):
        new_data = []
        for uf in data:
            date = uf['date']
            if not UF.objects.filter(date=date).exists():
                new_data.append({'date': date, 'value': uf['value']})
        return new_data

    @transaction.atomic
    def save_all(self, data):
        for uf in data:
            entry = UF(date=uf['date'], value=uf['value'])
            entry.save()


class UFtoCLP(APIView):

    def get_uf(self, date):
        try:
            ymd = list(map(int, date.split('-')))
            obj_date = datetime.date(ymd[0], ymd[1], ymd[2])
            if not UFtoCLP.available(obj_date):
                print("not available")
                raise ValueError
            return UF.objects.get(pk=date)
        except ValueError:
            raise Http404
        except UF.DoesNotExist:
            return None

    @staticmethod
    def available( obj_date):
        today = datetime.datetime.today()
        if today.month == 12:
            if today.day >= 10:
                return obj_date <= datetime.date(today.year + 1, 1, 9)
            else:
                return obj_date <= datetime.date(today.year, 12, 9)
        else:
            if today.day >= 10:
                return obj_date <= datetime.date(today.year, today.month + 1, 9)
            else:
                return obj_date <= datetime.date(today.year, today.month, 9)

    def get(self, request):
        date = request.query_params['date']
        amount = int(request.query_params['value'])
        uf = self.get_uf(date)
        if uf:
            clp = uf.getCLP(amount)
            return Response(float(clp))
        else:
            start_year = UF.objects.last().date.year
            end_year = datetime.datetime.now().year
            UFSpider.run(start_year, end_year)
        uf = self.get_uf(date)
        if uf:
            clp = uf.getCLP(amount)
            return Response(float(clp))

