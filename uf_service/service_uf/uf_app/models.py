from django.db import models
import datetime
from django.http import Http404


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
            if today.day >= 9:
                return date <= datetime.date(today.year + 1, 1, 9)
            else:
                return date <= datetime.date(today.year, 12, 9)
        else:
            if today.day >= 9:
                return date <= datetime.date(today.year, today.month + 1, 9)
            else:
                return date <= datetime.date(today.year, today.month, 9)

    @staticmethod
    def filter(data):
        new_data = []
        for uf in data:
            date = uf['date']
            if not UF.objects.filter(date=date).exists():
                new_data.append({'date': date, 'value': uf['value']})
        return new_data
