import os
import datetime
import stripe
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DetailView, TemplateView

from ..profiles.models import User
from .contracts import PoolContract
from .forms import PoolForm, TokenTypeForm
from .models import Pool, TokenType


class PoolsListView(TemplateView):
    template_name = 'clients/pools_list.pug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pc = PoolContract()
        ctx['keys'] = pc.get_pool_keys()
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
        pc = PoolContract()
        ctx = super().get_context_data(**kwargs)
        ctx['poolContractAddress'] = pc.address
        if ctx['object']['amountOfOffers'] > 0:
            ctx['offerStats'] = pc.get_offer_statistics(key=ctx['object']['key'])
        print(ctx)
        return ctx


class PoolOffersListView(DetailView):
    template_name = 'clients/pools_offers_list.pug'

    def get_object(self, queryset=None):
        pc = PoolContract()
        try:
            pool = pc.get_pool_by_key(self.kwargs['key'], mapped=True)
            return pool
        except Exception:
            raise Http404()

    def get_context_data(self, **kwargs):
        pc = PoolContract()
        ctx = super().get_context_data(**kwargs)
        ctx['offers'] = pc.get_offers_by_key(self.kwargs['key'])
        ctx['pool'] = pc.get_pool_by_key(self.kwargs['key'], mapped=True)
        ctx['stripeKey'] = os.environ.get('STRIPE_TEST_KEY')
        return ctx


class AdminPoolCreateView(TemplateView):
    template_name = 'admins/create_pool.pug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pc = PoolContract()
        ctx['available_tokens'] = TokenType.objects.all()
        pools = pc.get_all_pools()
        ctx['used_tokens'] = [pool['tokenName'] for pool in pools]
        print(ctx)
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


class AdminTokenTypeCreateView(TemplateView):
    template_name = 'admins/create_token_type.pug'

    def post(self, request):
        data = request.POST.copy()
        form = TokenTypeForm(data)
        if form.is_valid():
            form.save()
            return redirect(reverse('profiles:home'))
        print(form.errors)


@require_http_methods(["POST", ])
def pay_withdraw_view(request):
    if not request.is_ajax():
        return JsonResponse({'message': 'Error handler content'}, status=403)
    try:
        print(request.POST)
        index = int(request.POST['index'])
        token_qty = int(request.POST['amount'])
        key = request.POST['key']
        user_address = request.POST['account']
        token = request.POST['token']

        # Credit card info
        pc = PoolContract()
        pool = pc.get_pool_by_key(request.POST['key'], mapped=True)
        offer = pc.get_offer_by_index(index)
        stripe.api_key = os.environ.get('STRIPE_API_KEY')
        stripe.Charge.create(
            amount=token_qty * int(float(offer['offeredValue']) * 100),
            currency="usd",
            description="Cargo de compra de {} tokens".format(token_qty),
            source=token,
        )
        pc.withdraw_from_offer(index, token_qty * (10 ** int(offer['offeredDecimals'])), pool['tokenAddress'], user_address)
        response = HttpResponse('Success')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'There was an error'}, status=500)
