from django import forms
from .models import Currency


class ExchangeForm(forms.Form):
    currency_codes = [(currency.code, currency.code) for currency in Currency.objects.all()]
    currency_codes.append(('PLN', "PLN"))


    currency1_amount = forms.FloatField(label='Currency Amount', max_value=99999, min_value=0.5,
                                        widget=forms.NumberInput(attrs={'onkeyup': "sendRequest()", 'onchange': "sendRequest()"}))
    currency1_code = forms.ChoiceField(label='Currency Code', choices=currency_codes,
                                       widget=forms.Select(attrs={'onchange': "sendRequest()"}))
    currency2_amount = forms.FloatField(label='Calculated Amount', min_value=0.5, required=False, disabled=True)
    currency2_code = forms.ChoiceField(label='Currency to Calculate', choices=currency_codes,
                                       widget=forms.Select(attrs={'onchange': "sendRequest()"}))


class NumberOfMeasuringPointsForm(forms.Form):
    points = [
        (5, 5),
        (10, 10),
        (15, 15),

    ]
    points = forms.ChoiceField(label='Choice value of last measuring points: ', choices=points, initial=10, widget = forms.Select(attrs={'onchange': "sendRequest()"}))
