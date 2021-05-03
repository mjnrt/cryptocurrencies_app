import requests
import json
from .models import CurrentPrices
from django.core.exceptions import ObjectDoesNotExist


def my_api_schedule():
    # currencies = []
    # response = requests.get('https://api.bitbay.net/rest/trading/stats')
    url = "https://api.bitbay.net/rest/trading/stats"
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    current_prices = response.json()['items']
    for v in current_prices.values():
        market_symbol = v['m']
        lowest_price = v['l']
        highest_price = v['h']
        average_price = v['r24h']
        if market_symbol[-3:] == 'PLN' or market_symbol[-3:] == 'EUR' or market_symbol[-3:] == 'USD' or market_symbol[
                                                                                                        -3:] == 'GBP':
            try:
                update_currencie = CurrentPrices.objects.get(market_symbol=market_symbol)
                update_currencie.lowest_price = lowest_price
                update_currencie.highest_price = highest_price
                update_currencie.average_price = average_price
            except ObjectDoesNotExist:
                CurrentPrices.objects.create(market_symbol=market_symbol,
                                             lowest_price=lowest_price,
                                             highest_price=highest_price,
                                             average_price=average_price)
            # currencies.append([market_symbol, lowest_price, highest_price, average_price])
    return CurrentPrices.objects.all()

