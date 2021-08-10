from rest_framework import serializers


class RatesSerializer(serializers.ListField):
    no = serializers.CharField(max_length=15)
    effectiveDate = serializers.DateField()
    mid = serializers.FloatField()


class CurrencyExchangeSerializer(serializers.Serializer):
    table = serializers.CharField(default='A', max_length=1)
    currency = serializers.CharField(max_length=30)
    code = serializers.CharField(max_length=3)
    rates = RatesSerializer()


