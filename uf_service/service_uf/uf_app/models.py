from django.db import models


class UF(models.Model):
    date = models.DateField(db_index=True, primary_key=True)
    value = models.DecimalField(max_digits=7, decimal_places=2)

    def getCLP(self, amount):
        return self.value * amount
