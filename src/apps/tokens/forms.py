from django import forms

from apps.core.forms import BootstrapForm, BootstrapModelForm

from .models import Pool


class TokenBuyClass(BootstrapForm):
    quantity = forms.DecimalField(label='Cantidad')


class HelloWorldTestForm(BootstrapForm):
    text = forms.CharField(label='Entrada', max_length=100)
