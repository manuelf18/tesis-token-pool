from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView

from .forms import HelloWorldTestForm, TokenBuyClass
from .models import Pool
from .contract import Contract


class BuyerTemplateView(TemplateView):
    template_name = 'buy_list.pug'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['pools'] = Pool.objects.all()
        return ctx


class BuyTokenView(TemplateView):
    template_name = 'buy_form.pug'


class TestHelloWorldFormView(CreateView):
    template_name = 'test_blockchain_contract.pug'
    form_class = HelloWorldTestForm
    success_url = '/'
