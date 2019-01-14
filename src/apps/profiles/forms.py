from apps.core.forms import BootstrapModelForm
from django.forms import PasswordInput

from .models import User


class UserModelForm(BootstrapModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'identification', 'location')
        widgets = {
            'password': PasswordInput
        }
