import datetime
import os

import stripe
from django.core import serializers
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DetailView, TemplateView

from ..profiles.models import User
from .contracts import PoolContract, TokenContract
from .forms import PoolForm, TokenTypeForm
from .models import Pool, TokenType, Transaction


class PoolsListView(TemplateView):
    template_name = 'clients/pools_list.pug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pc = PoolContract()
        ctx['pools'] = pc.get_all_pools()
        return ctx


class PoolsDetailView(TemplateView):
    template_name = 'clients/pools_detail.pug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['id'] = kwargs['id']
        return ctx


class PoolOffersCreateView(DetailView):
    template_name = 'clients/pools_offers_create.pug'

    def get_object(self, queryset=None):
        pc = PoolContract()
        try:
            pool = pc.get_pool_by_key(self.kwargs['key'], mapped=True)
            return pool
        except Exception:
            raise Http404()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['poolContractAddress'] = TokenContract.get_pool_address()
        return ctx


class PoolOffersListView(DetailView):
    template_name = 'clients/pools_offers_list.pug'

    def get_object(self, queryset=None):
        pc = PoolContract()
        try:
            pool = pc.get_pool_by_key(self.kwargs['key'], mapped=True)
            return pool
        except Exception as e:
            print(e)
            raise Http404()

    def get_context_data(self, **kwargs):
        pc = PoolContract()
        ctx = super().get_context_data(**kwargs)
        ctx['offers'] = pc.get_offers_clean(self.kwargs['key'])
        ctx['pool'] = pc.get_pool_by_key(self.kwargs['key'], mapped=True)
        ctx['stripeKey'] = os.environ.get('STRIPE_TEST_KEY')
        return ctx


class AdminPoolCreateView(TemplateView):
    template_name = 'admins/create_pool.pug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pc = PoolContract()
        tokens = TokenType.objects.all()
        for token in tokens:
            tc = TokenContract(token.name)
            token.value = tc.get_current_token_value()
        pools = pc.get_all_pools()
        ctx['available_tokens'] = tokens
        ctx['used_tokens'] = [pool['tokenName'] for pool in pools]
        return ctx

    def post(self, request):
        data = request.POST.copy()
        data.pop('', None)
        data['admin'] = self.request.user.pk
        data['token_value'] = data.get('token_value', 1)
        form = PoolForm(data)
        if form.is_valid():
            try:
                pool = form.save()
            except Exception as e:
                print(e)
                return render(request, self.template_name)
            return redirect(reverse('profiles:home'))
        print(form.errors)
        return render(request, self.template_name)


class AdminTokenTypeList(TemplateView):
    template_name = 'admins/tokens_list.pug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tokens = TokenType.objects.all()
        for token in tokens:
            tc = TokenContract(token.name)
            token.balanceOf = tc.balanceOf(TokenContract.get_pool_address()) * 10 ** -2
            token.value = tc.get_current_token_value()
            pool_for_token = tc.get_pool_by_address()
            if pool_for_token and pool_for_token['open']:
                token.hasPool = True
            else:
                token.hasPool = False
        ctx['tokens'] = tokens
        return ctx


class AdminPoolListView(TemplateView):
    template_name = 'admins/pool_list.pug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pc = PoolContract()
        ctx['pools'] = pc.get_all_pools()
        print(ctx)
        return ctx


class AdminTokenTypeCreateView(TemplateView):
    template_name = 'admins/create_token_type.pug'

    def post(self, request):
        data = request.POST.copy()
        form = TokenTypeForm(data)
        if form.is_valid():
            form.save()
            return redirect(reverse('profiles:home'))
        print(form.errors)


@require_http_methods(["GET", ])
def get_transactions_by_address(request):
    if not request.is_ajax():
        return JsonResponse({'message': 'Error handler content'}, status=403)
    try:
        account = request.GET['account']
        tsx = Transaction.objects.filter(address=account)[:5]
        data = serializers.serialize('json', tsx)
        return HttpResponse(data, content_type="application/json")
    except Exception as e:
        print(e)
        return []


@require_http_methods(["POST", ])
def create_transaction(request):
    if not request.is_ajax():
        return JsonResponse({'message': 'Error handler content'}, status=403)
    try:
        pc = PoolContract()
        key = request.POST['key']
        email = request.POST['email']
        amount = float(request.POST['amount'])
        decimals = int(request.POST['decimals'])
        address = request.POST['tokenAddress']
        value = pc.get_current_token_value(address)
        account = request.POST['account']
        params = {
            'address': account,
            'transaction_type': Transaction.DEPOSIT,
            'amount': amount * 10 ** -decimals,
            'value': value
        }
        pc.create_offer(key, email, amount, decimals, account, value, address)
        Transaction.objects.create(**params)
        return HttpResponse('success')
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'There was an error'}, status=500)


@require_http_methods(["POST", ])
def pay_withdraw_view(request):
    if not request.is_ajax():
        return JsonResponse({'message': 'Error handler content'}, status=403)
    try:
        index = int(request.POST['index'])
        token_qty = float(request.POST['amount'])
        key = request.POST['key']
        user_address = request.POST['account']
        token = request.POST['token']

        # Credit card info
        pc = PoolContract()
        pool = pc.get_pool_by_key(request.POST['key'], mapped=True)
        offer = pc.get_offer_by_index(index)
        stripe.api_key = os.environ.get('STRIPE_API_KEY')

        """
        the stripe.Charge.create function takes the amount param in the form of the
        tiniest denomination of set currency available. So in case of making the transaction
        in USD, the amount must first be converted from USD to cents. 
        """
        stripe.Charge.create(
            amount=int(token_qty * float(offer['offeredValue']) * 100),
            currency="usd",
            description="Cargo de compra de {} tokens".format(token_qty),
            source=token,
        )
        pc.withdraw_from_offer(index, int(token_qty * (10 ** offer['offeredDecimals'])), pool['tokenAddress'], user_address)
        params = {
            'address': user_address,
            'transaction_type': Transaction.WITHDRAW,
            'amount': token_qty,
            'value': offer['offeredValue'],
        }
        Transaction.objects.create(**params)
        response = HttpResponse('Success')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'There was an error'}, status=500)


@require_http_methods(["POST", ])
def change_pool_status(request):
    if not request.is_ajax():
        return JsonResponse({'message': 'Error handler content'}, status=403)
    try:
        key = request.POST['key']
        pc = PoolContract()
        pc.close_pool(key)
        response = HttpResponse('Success')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'There was an error'}, status=500)
