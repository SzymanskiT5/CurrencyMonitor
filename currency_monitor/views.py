import io

import requests
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView, DetailView
from rest_framework.parsers import JSONParser

from .forms import ExchangeForm, NumberOfMeasuringPointsForm
from djangoProject.settings import NBP_COURSE_URL
from .models import Currency
from .serializers import CurrencyExchangeSerializer
from .vizualization import get_plot


def process_data_from_response(response):
    stream = io.BytesIO(response)
    data = JSONParser().parse(stream)
    return data


class CalculatorView(FormView):
    model = Currency
    form_class = ExchangeForm
    template_name = 'currency_exchange/calculator.html'
    context_object_name = "currencies"


class CurrencyView(DetailView):
    model = Currency
    slug_field = 'slug'
    slug_url_kwarg = 'code'
    form_class = NumberOfMeasuringPointsForm

    def set_serializing_error(self):
        messages.info(self.request, "Something went wrong")
        return render(self.request, 'currency_exchange/calculator.html')


    def create_serializer_object(self, response):
        data = process_data_from_response(response)
        serializer = CurrencyExchangeSerializer(data=data)
        return serializer

    def get_values_to_create_plot(self, serializer, currency):
        x_range = [objects['effectiveDate'] for objects in serializer.data['rates']]
        y_range = [objects['mid'] for objects in serializer.data['rates']]
        plot = get_plot(x_range, y_range, currency.code)
        return plot


    def get_response_from_API(self, currency, points = None):
        if not points:
            url = f"{NBP_COURSE_URL}{currency.code}/last/10/"
        else:
            url = f"{NBP_COURSE_URL}{currency.code}/last/{points}/"
        response = requests.get(url, params={'format': 'json'}).content
        return response

    def get(self, points=10, *args, **kwargs):
        currency = self.get_object()
        response = self.get_response_from_API(currency)
        serializer = self.create_serializer_object(response)
        if serializer.is_valid():
            plot = self.get_values_to_create_plot(serializer, currency)
            return render(self.request, 'currency_exchange/currency_status.html', {"plot": plot, "form":self.form_class()})

        return self.set_serializing_error()

    def post(self, *args, **kwargs):

        currency = self.get_object()
        points = self.request.POST.get('points')
        response = self.get_response_from_API(currency, points)
        serializer = self.create_serializer_object(response)
        if serializer.is_valid():
            plot = self.get_values_to_create_plot(serializer, currency)
            return render(self.request, 'currency_exchange/currency_status.html',
                          {"plot": plot, "form": self.form_class(self.request.POST)})

        return self.set_serializing_error()



def home(request) -> HttpResponse:
    return render(request, "currency_exchange/home.html", {"title": "DjangoCatering"})