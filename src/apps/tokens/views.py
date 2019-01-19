from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView
from .models import Pool

# from .forms import UserModelForm


class BuyerTemplateView(TemplateView):
    template_name = 'buyers.pug'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['pools'] = Pool.objects.all()
        return ctx


class BuyTokenView(CreateView):
    template_name = 'buy_token_form.pug'
