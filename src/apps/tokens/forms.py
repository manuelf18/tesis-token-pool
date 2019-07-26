from django import forms

from ..core.forms import BootstrapForm, BootstrapModelForm

from .models import Pool, TokenType


class PoolForm(BootstrapModelForm):
    class Meta:
        model = Pool
        fields = '__all__'

    def save(self, avoid_signals=False):
        pool = super().save(commit=False)
        pool._avoid_signals = avoid_signals
        return pool


class TokenTypeForm(BootstrapModelForm):
    class Meta:
        model = TokenType
        fields = '__all__'
