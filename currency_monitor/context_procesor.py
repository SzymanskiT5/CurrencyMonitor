from typing import Dict, Any

from django.http import HttpResponse

from currency_monitor.models import Currency

"""With context_processor we are able to use Currency model without the view"""
def currency(request) -> Dict[str, Any]:
    currencies_url = Currency.objects.all()
    return {"currencies": currencies_url}
