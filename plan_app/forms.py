from django import forms
from .models import Employees, Work


class RaportForm(forms.Form):
    worker = forms.ModelChoiceField(
        queryset=Employees.objects.all(),
        label='Worker'
    )
    task = forms.ModelChoiceField(
        queryset=Work.objects.all(),
        label='Task'
    )
    time = forms.FloatField(
        min_value=0.25,
        label='Time(h)'
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


class ExpenseForm(forms.Form):
    description = forms.CharField(
        max_length=255,
        label='Description'
    )
    quantity = forms.IntegerField(label='Quantity')
    price = forms.FloatField(label='Price for piece')