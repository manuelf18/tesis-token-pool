from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import DashboardView, HomeView, LoginView, SignUpView

app_name = 'profiles'

urlpatterns = [
    # client views
    path('', (HomeView.as_view()), name='home'),
    path('login', (LoginView.as_view()), name='login'),
    path('logout', (LogoutView.as_view(template_name='index.pug')), name='logout'),
    path('signup', (SignUpView.as_view()), name='signup'),


    # admin views
    path('dashboard', login_required(DashboardView.as_view()), name='home'),
]
