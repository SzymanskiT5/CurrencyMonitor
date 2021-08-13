from django.urls import path, include

from REST.views import CalculateViewAPI

urlpatterns = [
    path('currency-calculator/', CalculateViewAPI.as_view(), name='request_calculate'),

]
