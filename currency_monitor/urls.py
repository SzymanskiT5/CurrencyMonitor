from django.urls import path, include

from currency_monitor.views import HomeView, CurrencyView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("<slug:code>/", CurrencyView.as_view(), name='currency_details')
]
