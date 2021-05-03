import requests
import json
from datetime import datetime, timezone


def my_historical_prices_api(from_time, to_time, interval):
    if to_time == "now":
        to_timestamp = str(round(datetime.timestamp(datetime.now()))) + "000"
    else:
        to_timestamp = str(round(datetime.timestamp(datetime.strptime(to_time, "%Y-%m-%d %H:%M:%S"))))+"000"
    from_timestamp = str(round(datetime.timestamp(datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S"))))+"000"

    url = f"https://api.bitbay.net/rest/trading/candle/history/BTC-PLN/{interval}?from={from_timestamp}&to={to_timestamp}"
    response = requests.request("GET", url)

    historical_prices = []
    for item in response.json()['items']:
        historical_prices.append([datetime.fromtimestamp(int(item[0][0:10])), item[1]['c']])

    return historical_prices


print(my_historical_prices_api('2021-05-03 14:00:00', '2021-05-03 14:45:00', 900))
