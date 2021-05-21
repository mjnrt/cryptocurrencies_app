from django.db import models


class CurrentPrices(models.Model):
    market_symbol = models.CharField(max_length=50)
    lowest_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    highest_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)


class Users(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)  # need to add hashing
    premium_status = models.BooleanField(default=False)
