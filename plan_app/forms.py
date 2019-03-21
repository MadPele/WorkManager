from django import forms
from .models import ProductionLine


class RaportForm(forms.Form):
    production_line = forms.ModelChoiceField(
        queryset=ProductionLine.objects.all(),
        label='Production line'
    )
    time = forms.FloatField(
        min_value=0.25,
        label='Time'
    )
    quantity = forms.FloatField(
        min_value=1,
        label='Made pieces'
    )
    date = forms.DateField(label='Date')


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=55,
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput
    )
