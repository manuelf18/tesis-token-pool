import os

import stripe
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, TemplateView

from .contracts import PoolContract
from .forms import HelloWorldTestForm, TokenBuyClass
from .models import Pool


class PoolsListView(TemplateView):
    template_name = 'clients/pools_list.pug'


class PoolsDetailView(TemplateView):
    template_name = 'clients/pools_detail.pug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['id'] = kwargs['id']
        return ctx


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


@require_http_methods(["POST", ])
def pay_withdraw_view(request):
    if not request.is_ajax():
        return JsonResponse({'message': 'Error handler content'}, status=403)
    try:
        token_qty = int(request.POST['token_qty'])
        pool_index = int(request.POST['pool_index'])
        user_address = request.POST['user_address']
        pool = PoolContract()
        stripe.api_key = os.environ.get('STRIPE_API_KEY')
        stripe.Charge.create(
            amount=token_qty * 100,
            currency="usd",
            description="Cargo de compra de {} tokens".format(token_qty),
            source="tok_amex",
            )
        pool.pay_user_for_withdrawing_pool(pool_index, token_qty, user_address)
        response = HttpResponse('Success')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'There was an error'}, status=500)


@require_http_methods(["POST", ])
def pay_deposit_view(request):
    if not request.is_ajax():
        return JsonResponse({'message': 'Error handler content'}, status=403)
    try:
        print(request.POST)
        token_qty = int(request.POST['qty'])
        user_address = request.POST['user_address']
        pool = PoolContract()
        pool.pay_user_for_joining_pool(user_address, token_qty)
        response = HttpResponse('Success')
        response.status_code = 200
        return response
    except:
        return JsonResponse({'message': 'There was an error'}, status=500)
