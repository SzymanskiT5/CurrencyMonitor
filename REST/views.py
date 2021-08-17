import io
import requests
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from currency_monitor.vizualization import get_plot
from .serializers import CurrencyExchangeSerializer, NBPResponseSerializer
from djangoProject.settings import NBP_COURSE_URL


def process_data_from_response(response) -> bytes:
    stream = io.BytesIO(response)
    data = JSONParser().parse(stream)
    return data


class CalculateViewAPI(APIView):

    def set_response(self, value) -> HttpResponse:
        value = round(value, 2)
        data = {"value": value}
        serializer = CurrencyExchangeSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data)

        return self.set_serializing_error(serializer)

    def set_serializing_error(self, serializer) -> HttpResponse:
        return Response(serializer.errors)

    def change_pln_to_currency(self, currency2_code, currency1_amount)-> HttpResponse:
        response = requests.get(NBP_COURSE_URL + currency2_code, params={"format": 'json'}).content
        data = process_data_from_response(response)
        serializer = NBPResponseSerializer(data=data)
        if serializer.is_valid():
            currency2_value = serializer.data['rates'][0]['mid']
            result = ((currency1_amount * 1000) / (currency2_value * 1000))
            return self.set_response(result)

        return self.set_serializing_error(serializer)

    def change_currency_to_pln(self, currency1_code, currency1_amount)-> HttpResponse:
        response = requests.get(NBP_COURSE_URL + currency1_code, params={"format": 'json'}).content
        data = process_data_from_response(response)
        serializer = NBPResponseSerializer(data=data)
        if serializer.is_valid():
            currency1_value = serializer.data['rates'][0]['mid']
            result = (currency1_value * currency1_amount)
            return self.set_response(result)

        return self.set_serializing_error(serializer)

    def change_currency_to_currency(self, currency1_code, currency2_code, currency1_amount) -> HttpResponse:
        payload = {"format": 'json'}
        response_1 = requests.get(NBP_COURSE_URL + currency1_code, params=payload).content
        data_1 = process_data_from_response(response_1)
        response_2 = requests.get(NBP_COURSE_URL + currency2_code, params=payload).content
        data_2 = process_data_from_response(response_2)
        serializer_1 = NBPResponseSerializer(data=data_1)
        serializer_2 = NBPResponseSerializer(data=data_2)

        if serializer_1.is_valid() and serializer_2.is_valid():
            currency1_value = serializer_1.data['rates'][0]['mid']
            currency2_value = serializer_2.data['rates'][0]['mid']
            result = ((currency1_value * currency1_amount * 1000) / (currency2_value * 1000))
            return self.set_response(result)

        if serializer_1.errors:
            return self.set_serializing_error(serializer_1)
        elif serializer_2.errors:
            return self.set_serializing_error(serializer_1)

    def post(self, request) -> HttpResponse:
        data = request.data
        currency1_amount = float(data.get("currency1_amount"))
        currency1_code = data.get("currency1_code")
        currency2_code = data.get("currency2_code")

        if currency2_code == currency1_code:
            return self.set_response(currency1_amount)

        elif currency1_code == "PLN":
            return self.change_pln_to_currency(currency2_code, currency1_amount)

        elif currency2_code == "PLN":
            return self.change_currency_to_pln(currency1_code, currency1_amount)

        return self.change_currency_to_currency(currency1_code, currency2_code, currency1_amount)


class PlotViewAPI(APIView):

    def create_serializer_object(self, response)-> NBPResponseSerializer:
        data = process_data_from_response(response)
        serializer = NBPResponseSerializer(data=data)
        return serializer

    def get_values_to_create_plot(self, serializer, currency) -> str:
        x_range = [objects['effectiveDate'] for objects in serializer.data['rates']]
        y_range = [objects['mid'] for objects in serializer.data['rates']]
        plot = get_plot(x_range, y_range, currency.upper())
        return plot

    def post(self, request) -> HttpResponse:
        data = request.data
        points = data.get('points')
        currency_code = data.get('currency_code')
        url = f"{NBP_COURSE_URL}{currency_code}/last/{points}/"
        response = requests.get(url, params={'format': 'json'}).content
        serializer = self.create_serializer_object(response)
        if serializer.is_valid():
            plot = self.get_values_to_create_plot(serializer, currency_code)
            response = {'plot': plot}
            return Response(response)
