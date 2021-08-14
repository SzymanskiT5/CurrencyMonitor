from rest_framework import serializers


class CurrencyExchangeSerializer(serializers.Serializer):
    value = serializers.FloatField()



class NBPResponseSerializer(serializers.Serializer):
    table = serializers.CharField(default='A', max_length=1)
    currency = serializers.CharField(max_length=30)
    code = serializers.CharField(max_length=3)
    rates = serializers.ListField()


class PlotSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=3)
    points = serializers.IntegerField()