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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password', None)
        confirm_password = cleaned_data.pop('confirm_password', None)
        if password is None or confirm_password is None:
            raise forms.ValidationError("Password should not be empty")
        elif password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
