from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView

import stripe

from .contracts import PoolContract
from .forms import HelloWorldTestForm, TokenBuyClass
from .models import Pool


class TokensListView(TemplateView):
    template_name = 'clients/tokens_list.pug'


class BuyerTemplateView(TemplateView):
    template_name = 'buy_list.pug'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['pools'] = Pool.objects.all()
        return ctx


class BuyTokenView(TemplateView):
    template_name = 'buy_form.pug'


class GetTokenView(TemplateView):
    template_name = 'get_tokens_form.pug'


class StatusView(TemplateView):
    template_name = 'status_view.pug'


# class PayView(TemplateView):

#     def get_context_data(self, *args, **kwargs):
#         print(self.request.POST)
#         return super().get_context_data(kwargs)


""" This is the only function based view in this project,
    because it's only goal is to comunicate with the Contract class """


def pay_view(request):
    if request.method == 'POST':
        token_qty = request.POST.get('qty', None)
        pool_index = request.POST.get('pool_index', None)
        if (token_qty is None or pool_index is None):
            response = HttpResponse('Failure')
            response.status_code = 400
            return response
        try:
            token_qty = int(token_qty)
            pool_index = int(pool_index)
            stripe.api_key = "sk_test_KuzPN3hC3fKgYD8KljCMkZ2F"
            stripe.Charge.create(
                amount=token_qty,
                currency="usd",
                description="Cargo de compra de {} tokens".format(token_qty / 100),
                source="tok_amex",
            )
            pool = PoolContract()
            pool.pay(pool_index, token_qty)
            response = HttpResponse('Success')
            response.status_code = 200
            return response
        except:
            raise Exception('Hubo un error')
    return HttpResponse('Wrong Method').status_code(405)
