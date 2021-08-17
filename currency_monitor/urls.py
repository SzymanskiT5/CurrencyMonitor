from django.urls import path
from currency_monitor import views
from currency_monitor.views import CalculatorView, CurrencyView

urlpatterns = [
    path('', views.home, name='home'),
    path('calculator/', CalculatorView.as_view(), name='calculator'),
    path("<slug:code>/", CurrencyView.as_view(), name='currency_details')
]
