from django import forms

class ExchangeForm(forms.Form):

    currency_codes = [
        ("PLN","PLN"),
        ("USD","USD"),
        ("EUR", "EUR"),
        ("GBP", "GBP"),
        ("RUB", "RUB"),
        ("CNY", "CNY")
    ]




    currency1_amount = forms.FloatField(label='Currency Amount', max_value=99999, min_value=0.5)
    currency1_code = forms.ChoiceField(label='Currency Code',choices=currency_codes)
    currency2_amount =forms.FloatField(label='Calculated Amount',min_value=0.5, required=False, disabled=True)
    currency2_code = forms.ChoiceField(label='Currency to Calculate', choices=currency_codes)

