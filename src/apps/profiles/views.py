from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView

from .forms import UserModelForm


class HomeView(TemplateView):
    template_name = 'index.pug'


class LoginView(DjangoLoginView):
    template_name = 'login.pug'
    success_url = '/'


class SignUpView(CreateView):
    form_class = UserModelForm
    template_name = "signup.pug"
    success_url = '/'

    def form_valid(self, form, *args, **kwargs):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        return redirect(self.success_url)
