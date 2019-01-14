from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import UserModelForm


class HomeView(TemplateView):
    template_name = 'index.pug'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['is_logged'] = False
        return ctx


class LoginView(TemplateView):
    template_name = 'login.pug'


class SignUpView(CreateView):
    form_class = UserModelForm
    template_name = "signup.pug"
    success_url = '/'
