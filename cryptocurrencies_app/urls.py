"""cryptocurrencies_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dashboard.views import LandingPage, ListPage, SingleCryptoPage, PredictionPage, DataTablePage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing'),
    path('list/', ListPage.as_view(), name='list'),
    path('list/<int:currencie_id>/', SingleCryptoPage.as_view(), name='crypto'),
    path('list/<int:currencie_id>/predykcja/', PredictionPage.as_view(), name='predicting'),
    path('list/<int:currencie_id>/tabela-danych/', DataTablePage.as_view(), name='data-table'),
]
