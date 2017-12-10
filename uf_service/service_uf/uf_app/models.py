from django.db import models
import datetime
from django.http import Http404
from uf_app.constants import *


class UF(models.Model):
    date = models.DateField(db_index=True, primary_key=True)
    value = models.DecimalField(max_digits=7, decimal_places=2)

    def get_price(self, amount):
        return self.value * amount

    @staticmethod
    def get(date):
        try:
            ymd = list(map(int, date.split('-')))
            obj_date = datetime.date(ymd[0], ymd[1], ymd[2])  # throws ValueError
            if not UF.available(obj_date):
                raise ValueError
            return UF.objects.get(pk=date)
        except ValueError:
            raise Http404
        except UF.DoesNotExist:
            return None

    @staticmethod
    def available(date):
        today = datetime.datetime.today()
        if today.month == 12:
            if today.day > UF_UPDATE_DAY:
                return date <= datetime.date(today.year + 1, 1, UF_UPDATE_DAY)
            else:
                return date <= datetime.date(today.year, 12, UF_UPDATE_DAY)
        else:
            if today.day > UF_UPDATE_DAY:
                return date <= datetime.date(today.year, today.month + 1, UF_UPDATE_DAY)
            else:
                return date <= datetime.date(today.year, today.month, UF_UPDATE_DAY)

    @staticmethod
    def filter(data):
        new_data = []
        for uf in data:
            date = uf[DATE_FIELD]
            if not UF.objects.filter(date=date).exists():
                new_data.append({DATE_FIELD: date,
                                 VALUE_FIELD: uf[VALUE_FIELD]})
        return new_data
