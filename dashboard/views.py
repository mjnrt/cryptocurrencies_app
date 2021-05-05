from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import CurrentPrices
from .cron import my_api_schedule
from .services import my_historical_prices_api
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go


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
        last_year_data = my_historical_prices_api('2021-01-01 00:00:00', 'now', 3600, currencie.market_symbol[0:3],
                                                  currencie.market_symbol[-3:])
        ax = []
        ay = []
        for single_data in last_year_data:
            ax.append(str(single_data[0]))
            ay.append(float(single_data[1]))

        fig = go.Figure()
        # scatter1 = go.Scatter(x=ax, y=ay,
        #                       mode='lines', name='open',
        #                       opacity=0.8, marker_color='green')
        # fig.add_trace(scatter1)
        scatter2 = go.Scatter(x=ax, y=ay, mode='lines', name='close', opacity=0.8, marker_color='red')
        fig.add_trace(scatter2)
        plot_div = plot(fig, output_type='div')
        # plot_div = plot([Scatter(x=ax, y=ay,
        #                          mode='lines', name=currencie.market_symbol,
        #                          opacity=0.8, marker_color='blue')],
        #                 output_type='div')
        ctx = {'crypto': currencie,
               'plot': plot_div}
        return render(request, self.template_name, ctx)
