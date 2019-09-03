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
        return ctx


class AdminPoolCreateView(TemplateView):
    template_name = 'admins/create_pool.pug'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['available_tokens'] = TokenType.objects.all()
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
