from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView

from .forms import HelloWorldTestForm
from .models import Pool
from .contract import Contract

# from .forms import UserModelForm


class BuyerTemplateView(TemplateView):
    template_name = 'buyers.pug'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['pools'] = Pool.objects.all()
        return ctx


class BuyTokenView(CreateView):
    template_name = 'buy_token_form.pug'


class TestHelloWorldFormView(CreateView):
    template_name = 'test_blockchain_contract.pug'
    form_class = HelloWorldTestForm
    success_url = '/'

    def form_valid(self, form, *args, **kwargs):
        message = form.cleaned_data['text']
        contract = Contract().send_to_contract(message="Hola Mundo")
        print(contract)
        return redirect(self.success_url)
