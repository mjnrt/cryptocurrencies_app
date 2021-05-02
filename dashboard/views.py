from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import CurrentPrices
from .cron import my_api_schedule


class LandingPage(View):
    template_name = 'dashboard/landing.html'

    def get(self, request):
        prices = my_api_schedule()
        ctx = {'prices': prices}
        return render(request, self.template_name, ctx)

    def post(self, request):
        fiat = request.POST.get('fiat')
        prices = my_api_schedule()
        filtered_prices = []
        for price in prices:
            if fiat == 'PLN':
                if price.market_symbol[-3:] == 'PLN':
                    filtered_prices.append(price)
            elif fiat == 'EUR':
                if price.market_symbol[-3:] == 'EUR':
                    filtered_prices.append(price)
            elif fiat == 'GBP':
                if price.market_symbol[-3:] == 'GBP':
                    filtered_prices.append(price)
            elif fiat == 'USD':
                if price.market_symbol[-3:] == 'USD':
                    filtered_prices.append(price)
        ctx = {
            'prices': filtered_prices
        }
        return render(request, self.template_name, ctx)


class SingleCryptoPage(View):
    template_name = 'dashboard/single_crypto.html'

    def get(self, request, currencie_id):
        currencie = CurrentPrices.objects.get(pk=currencie_id)
        ctx = {'crypto': currencie}
        return render(request, self.template_name, ctx)
