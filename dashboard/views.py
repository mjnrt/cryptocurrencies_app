from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import CurrentPrices
from .cron import my_api_schedule
from .services import my_historical_prices_api
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go
from .services import predict_prices, get_plot
from datetime import datetime, timedelta


class LandingPage(View):
    template_name = 'dashboard/landing.html'

    def get(self, request):
        ctx = {}
        return render(request, self.template_name, ctx)


class FaqPage(View):
    template_name = "dashboard/faq.html"

    def get(self, request):
        return render(request, self.template_name)


class ListPage(View):
    template_name = 'dashboard/list.html'

    def get(self, request):
        prices = my_api_schedule()
        print(prices.reverse()[0].market_symbol, prices.reverse()[0].average_price)
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
    prediction_status = False

    def get(self, request, currencie_id):
        currencie = CurrentPrices.objects.get(pk=currencie_id)
        last_year_data = my_historical_prices_api('2021-01-01 00:00:00', 'now', 3600, currencie.market_symbol[0:3],
                                                  currencie.market_symbol[-3:])
        ax = []  # date [X]
        oy = []  # open price [Y]
        cy = []  # close price [Y]
        vy = []  # volume [Y]
        for single_data in last_year_data:
            ax.append(str(single_data[0]))
            oy.append(float(single_data[1]))
            cy.append(float(single_data[2]))
            vy.append(float(single_data[3]))

        layout = go.Layout(height=500, paper_bgcolor='#212529', plot_bgcolor='#212529', legend_font_color='white',
                           font_color='white', font_size=14)  # setting background plot color
        fig = go.Figure(layout=layout)
        fig.update_xaxes(gridcolor="#4D4D4D")
        fig.update_yaxes(gridcolor="#4D4D4D")
        fig.update_xaxes(dividercolor="red")
        scatter1 = go.Scatter(x=ax, y=oy, mode='lines', name='otwarcie', opacity=0.8, marker_color='#29FF00')
        fig.add_trace(scatter1)
        scatter2 = go.Scatter(x=ax, y=cy, mode='lines', name='zamknięcie', opacity=0.8, marker_color='#FF005A')
        fig.add_trace(scatter2)
        scatter3 = go.Scatter(x=ax, y=vy, mode='lines', name='wolumen', opacity=0.8, marker_color='#00F9FF')
        fig.add_trace(scatter3)
        plot_div = plot(fig, output_type='div')
        # plot_div = plot([Scatter(x=ax, y=ay,
        #                          mode='lines', name=currencie.market_symbol,
        #                          opacity=0.8, marker_color='blue')],
        #                 output_type='div')
        self.prediction_status = False
        ctx = {'crypto': currencie,
               'plot': plot_div,
               'prediction_status': self.prediction_status}
        return render(request, self.template_name, ctx)

    def post(self, request, currencie_id):
        prediction_currencie = request.POST.get('predict')
        if request.POST.get('predict'):
            return redirect(f'/list/{currencie_id}/predykcja/')
        elif request.POST.get('table-data'):
            return redirect(f'/list/{currencie_id}/tabela-danych')


class DataTablePage(View):
    template_name = "dashboard/data-table.html"

    def get(self, request, currencie_id):
        currencie = CurrentPrices.objects.get(pk=currencie_id)
        ctx = {"currencie": currencie}
        return render(request, self.template_name, ctx)

    def post(self, request, currencie_id):
        currencie = CurrentPrices.objects.get(pk=currencie_id)
        days_option = request.POST.get('days')
        if days_option == 'od początku roku':
            table_data = my_historical_prices_api('2021-01-01 00:00:00', "now", 86400, currencie.market_symbol[0:3],
                                                  currencie.market_symbol[-3:])
        else:
            dt1 = datetime.now() - timedelta(int(days_option))
            from_date = f"{dt1.year}-{dt1.month}-{dt1.day} {dt1.hour}:{dt1.minute}:{dt1.second}"
            table_data = my_historical_prices_api(from_date, "now", 86400, currencie.market_symbol[0:3],
                                                  currencie.market_symbol[-3:])
        table_data.reverse()
        ctx = {'table_data': table_data,
               'currencie': currencie}
        return render(request, self.template_name, ctx)


class PredictionPage(View):
    template_name = 'dashboard/predicting.html'

    def get(self, request, currencie_id):
        predicting_status = False
        currencie = CurrentPrices.objects.get(pk=currencie_id)
        ctx = {"currencie": currencie,
               "predicting": predicting_status}
        return render(request, self.template_name, ctx)

    def post(self, request, currencie_id):
        currencie = CurrentPrices.objects.get(pk=currencie_id)
        ctx = {}
        if "make-prediction" in request.POST:
            currencie_prices_len = len(
                my_historical_prices_api('2016-01-01 00:00:00', 'now', 86400, currencie.market_symbol[0:3],
                                         currencie.market_symbol[-3:]))
            if currencie_prices_len < 100:
                message = "Nie można wykonać predykcji. Waluta jest zbyt krótko na rynku aby przeanalizować jej zachowanie i przewidzieć trend."
                predicting_status = "can't do prediction"
                ctx = {"message": message,
                       "predicting": predicting_status}
            else:
                predicted_price, prediction_status, actual_prices, prediction_prices = predict_prices(
                    currencie.market_symbol[0:3], currencie.market_symbol[-3:])
                chart = get_plot(actual_prices, prediction_prices, currencie.market_symbol)
                if currencie.average_price > predicted_price:
                    message = "W najbliższym dniu kurs będzie maleć. To nie jest dobry moment na inwestycję."
                    img = 'decrease.png'
                else:
                    message = "Przewidywana cena jest wyższa. Zainwestuj teraz!"
                    img = 'increase.png'
                ctx = {"predicted_price": predicted_price,
                       "predicting": prediction_status,
                       "currencie": currencie,
                       "message": message,
                       "img": img,
                       "chart": chart}
                return render(request, self.template_name, ctx)
        return render(request, self.template_name, ctx)
