from django.urls import path, include

from REST.views import CalculateViewAPI, PlotViewAPI

urlpatterns = [
    path('currency-calculator/', CalculateViewAPI.as_view(), name='request_calculate'),
    path('currency-plot/', PlotViewAPI.as_view(), name='request_plot'),

]
