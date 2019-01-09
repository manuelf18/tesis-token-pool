from apps.core.forms import BootstrapModelForm

from .models import User


class UserModelForm(BootstrapModelForm):
    class Meta:
        model = User
        fields = ('email', 'name')
