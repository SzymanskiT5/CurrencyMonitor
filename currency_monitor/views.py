import json

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, FormView
from rest_framework.parsers import JSONParser

from .forms import ExchangeForm
from djangoProject.settings import NBP_COURSE_URL



class HomeView(FormView):
    form_class = ExchangeForm
    template_name = 'currency_exchange/home.html'

    def set_form_and_result(self, result):
        form = ExchangeForm(self.request.POST, initial={'currency2_amount': result})
        return render(self.request, 'currency_exchange/home.html', {"form": form, "result": result})

    def change_pln_to_currency(self, currency2_code, currency1_amount):
         response = requests.get(NBP_COURSE_URL + currency2_code, params={"format": 'json'}).text
         currency2_value = (json.loads(response)['rates'][0]['mid'])
         result = ((currency1_amount * 1000) / (currency2_value * 1000))
         result = round(result, 2)
         return self.set_form_and_result(result)


    def change_currency_to_pln(self, currency1_code, currency1_amount):
        response = requests.get(NBP_COURSE_URL + currency1_code, params={"format": 'json'}).text
        currency1_value = (json.loads(response)['rates'][0]['mid'])
        result = (currency1_value * currency1_amount)
        result = round(result, 2)
        return self.set_form_and_result(result)

    def change_currency_to_currency(self, currency1_code, currency2_code, currency1_amount):
        payload = {"format": 'json'}
        response_1 = requests.get(NBP_COURSE_URL + currency1_code, params=payload).text
        response_2 = requests.get(NBP_COURSE_URL + currency2_code, params=payload).text
        currency1_value = (json.loads(response_1)['rates'][0]['mid'])
        currency2_value = json.loads(response_2)['rates'][0]['mid']
        result = ((currency1_value * currency1_amount * 1000) / (currency2_value * 1000))
        result = round(result, 2)
        return self.set_form_and_result(result)


    def form_valid(self, form) -> HttpResponse:
        currency1_code = form.cleaned_data.get("currency1_code")
        currency2_code = form.cleaned_data.get("currency2_code")
        currency1_amount = form.cleaned_data.get("currency1_amount")

        if currency1_code == "PLN":
            return self.change_pln_to_currency(currency2_code, currency1_amount)

        elif currency2_code == "PLN":
            return self.change_currency_to_pln(currency1_code, currency1_amount)

        return self.change_currency_to_currency(currency1_code, currency2_code, currency1_amount)




