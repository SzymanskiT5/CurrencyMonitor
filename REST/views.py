import io
import requests
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CurrencyExchangeSerializer, NBPResponseSerializer
from djangoProject.settings import NBP_COURSE_URL




class CalculateViewAPI(APIView):

    def process_data_from_response(self, response):
        stream = io.BytesIO(response)
        data = JSONParser().parse(stream)
        return data

    def set_response(self, value):
        value = round(value, 2)
        data = {"value": value }
        serializer = CurrencyExchangeSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data)

        return self.set_serializing_error(serializer)


    def set_serializing_error(self, serializer):
        return Response(serializer.errors)


    def change_pln_to_currency(self, currency2_code, currency1_amount):
        response = requests.get(NBP_COURSE_URL + currency2_code, params={"format": 'json'}).content
        data = self.process_data_from_response(response)
        serializer = NBPResponseSerializer(data=data)
        if serializer.is_valid():
            currency2_value = serializer.data['rates'][0]['mid']
            result = ((currency1_amount * 1000) / (currency2_value * 1000))
            return self.set_response(result)

        return self.set_serializing_error(serializer)

    def change_currency_to_pln(self, currency1_code, currency1_amount):
        response = requests.get(NBP_COURSE_URL + currency1_code, params={"format": 'json'}).content
        data = self.process_data_from_response(response)
        serializer = NBPResponseSerializer(data=data)
        if serializer.is_valid():
            currency1_value = serializer.data['rates'][0]['mid']
            result = (currency1_value * currency1_amount)
            return self.set_response(result)

        return self.set_serializing_error(serializer)


    def change_currency_to_currency(self, currency1_code, currency2_code, currency1_amount):
        payload = {"format": 'json'}
        response_1 = requests.get(NBP_COURSE_URL + currency1_code, params=payload).content
        data_1 = self.process_data_from_response(response_1)
        response_2 = requests.get(NBP_COURSE_URL + currency2_code, params=payload).content
        data_2 = self.process_data_from_response(response_2)
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




    def post(self, request):
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

    def post(self, request):
        pass

