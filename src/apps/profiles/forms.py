from django import forms

from apps.core.forms import BootstrapModelForm

from .models import User


class UserModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'confirm_password', 'identification', 'location')
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        # do something
        if self.cleaned_data['password'] is not self.cleaned_data['confirm_password']:
            raise ValueError('Passwords do not match')
        super().save(commit=commit)
