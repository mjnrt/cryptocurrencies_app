from django.db import models


class CurrentPrices(models.Model):
    market_symbol = models.CharField(max_length=50)
    lowest_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    highest_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
