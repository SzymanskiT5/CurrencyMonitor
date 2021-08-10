from currency_monitor.models import Currency


def currency(request):
    currencies_url = Currency.objects.all()
    return {"currencies": currencies_url}