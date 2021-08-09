from django.urls import path, include

from currency_monitor.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home')
]
