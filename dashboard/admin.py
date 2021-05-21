from django.contrib import admin
from .models import CurrentPrices


@admin.register(CurrentPrices)
class CurrentPricesAdmin(admin.ModelAdmin):
    list_display = [
        'market_symbol', 'lowest_price', 'highest_price', 'average_price'
    ]
    fields = [
        'market_symbol',
        'lowest_price',
        'highest_price',
        'average_price',
    ]
