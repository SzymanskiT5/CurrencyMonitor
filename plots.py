import io
from datetime import date, timedelta
import requests
from matplotlib import pyplot as plt
from rest_framework.parsers import JSONParser
from currency_monitor.serializers import CurrencyExchangeSerializer

today = date.today()
ten_days = [today - timedelta(days=i) for i in range(11)]
ten_days.reverse()



url = f"http://api.nbp.pl/api/exchangerates/rates/a/chf/{ten_days[0]}/{ten_days[-1]}/"
response = requests.get(url).content
stream = io.BytesIO(response)
data = JSONParser().parse(stream)
serializer = CurrencyExchangeSerializer(data=data, many=True)
if serializer.is_valid():
    for objects in serializer.data['rates']:
        print(objects['mid'])
        plt.ylabel('Value')
        plt.xlabel('Dates')
    # values = serializer1.data['rates'][0]['mid']


# x_range = [i for i in range(11)]
#
#
#
# y_range = [1 for i in range(11)]
# plt.plot(x_range, y_range )
# plt.ylabel('Value')
# plt.xlabel('Dates')
# plt.show()