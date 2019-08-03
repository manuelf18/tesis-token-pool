from django import forms

from ..core.forms import BootstrapForm, BootstrapModelForm

from .models import Pool, TokenType
from .contracts import PoolContract


class PoolForm(BootstrapForm):
    name = forms.CharField()
    token_type = forms.IntegerField()

    def clean_token_type(self, *args, **kwargs):
        try:
            tc = TokenType.objects.get(pk=self.cleaned_data.get('token_type'))
            return tc
        except tc.DoesNotExist:
            raise ValueError('The token_type is invalid')
        except Exception as e:
            print(e)
            raise e

    def save(self):
        pool_name = self.cleaned_data['name']
        token_name = self.cleaned_data['token_type'].name
        pc = PoolContract()
        return pc.create_pool(pool_name, token_name)


class TokenTypeForm(BootstrapModelForm):
    class Meta:
        model = TokenType
        fields = '__all__'
