import json
import io
import requests
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, FormView
from rest_framework.parsers import JSONParser

from .forms import ExchangeForm
from djangoProject.settings import NBP_COURSE_URL
from .serializers import CurrencyExchangeSerializer


class HomeView(FormView):
    form_class = ExchangeForm
    template_name = 'currency_exchange/home.html'

    def set_form_and_result(self, result):
        result = round(result,2)
        form = ExchangeForm(self.request.POST, initial={'currency2_amount': result})
        return render(self.request, 'currency_exchange/home.html', {"form": form})

    def set_serializing_error(self):
        messages.info(self.request, "Something went wrong")
        return render(self.request, 'currency_exchange/home.html', {"form": self.form_class()})


    def change_pln_to_currency(self, currency2_code, currency1_amount):
        response = requests.get(NBP_COURSE_URL + currency2_code, params={"format": 'json'}).content
        stream = io.BytesIO(response)
        data = JSONParser().parse(stream)
        serializer = CurrencyExchangeSerializer(data=data)
        if serializer.is_valid():
            currency2_value = serializer.data['rates'][0]['mid']
            result = ((currency1_amount * 1000) / (currency2_value * 1000))
            return self.set_form_and_result(result)

        return self.set_serializing_error()




    def change_currency_to_pln(self, currency1_code, currency1_amount):
        response = requests.get(NBP_COURSE_URL + currency1_code, params={"format": 'json'}).content
        stream = io.BytesIO(response)
        data = JSONParser().parse(stream)
        serializer = CurrencyExchangeSerializer(data=data)
        if serializer.is_valid():
            currency1_value = serializer.data['rates'][0]['mid']
            result = (currency1_value * currency1_amount)
            return self.set_form_and_result(result)

        return self.set_serializing_error()

    def change_currency_to_currency(self, currency1_code, currency2_code, currency1_amount):
        payload = {"format": 'json'}
        response_1 = requests.get(NBP_COURSE_URL + currency1_code, params=payload).content
        stream1 = io.BytesIO(response_1)
        data1 = JSONParser().parse(stream1)
        response_2 = requests.get(NBP_COURSE_URL + currency2_code, params=payload).content
        stream2 = io.BytesIO(response_2)
        data2 = JSONParser().parse(stream2)
        serializer1 = CurrencyExchangeSerializer(data=data1)
        serializer2 = CurrencyExchangeSerializer(data=data2)
        if serializer1.is_valid() and serializer2.is_valid():
            currency1_value = serializer1.data['rates'][0]['mid']
            currency2_value = serializer2.data['rates'][0]['mid']
            result = ((currency1_value * currency1_amount * 1000) / (currency2_value * 1000))
            return self.set_form_and_result(result)

        return self.set_serializing_error()


    def form_valid(self, form) -> HttpResponse:
        currency1_code = form.cleaned_data.get("currency1_code")
        currency2_code = form.cleaned_data.get("currency2_code")
        currency1_amount = form.cleaned_data.get("currency1_amount")

        if currency1_code == "PLN":
            return self.change_pln_to_currency(currency2_code, currency1_amount)

        elif currency2_code == "PLN":
            return self.change_currency_to_pln(currency1_code, currency1_amount)

        return self.change_currency_to_currency(currency1_code, currency2_code, currency1_amount)




