import requests
import json


def get_current_prices():
    currencies = []
    # response = requests.get('https://api.bitbay.net/rest/trading/stats')
    url = "https://api.bitbay.net/rest/trading/stats"
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    current_prices = response.json()['items']
    for v in current_prices.values():
        market = v['m']
        price = v['r24h']
        currencies.append([market, price])
    return currencies


print(get_current_prices())
