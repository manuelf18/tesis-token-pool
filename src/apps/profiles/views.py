from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext
from django.views.generic import CreateView, TemplateView
from ..tokens.contracts import PoolContract

from .forms import UserModelForm


class HomeView(TemplateView):
    template_name = 'index.pug'


class LoginView(DjangoLoginView):
    template_name = 'login.pug'


class SignUpView(CreateView):
    form_class = UserModelForm
    template_name = "signup.pug"
    success_url = '/admin'

    def form_valid(self, form, *args, **kwargs):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        return redirect(self.success_url)


class DashboardView(TemplateView):
    template_name = 'dashboard.pug'


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pc = PoolContract()
        ctx['token_amount'] = pc.get_balance_of('TrueToken')
        print(ctx)
        return ctx
