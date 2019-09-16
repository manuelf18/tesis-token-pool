from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (AboutUsView, DashboardView, LandingView, HowItWorksView,
                    LoginView, SignUpView)

app_name = 'profiles'

urlpatterns = [
    # client views
    path('', LandingView.as_view(), name='landing'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(template_name='index.pug'), name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('about-us', AboutUsView.as_view(), name='about-us'),
    path('how-it-works', HowItWorksView.as_view(), name='how-it-works'),


    # admin views
    path('dashboard', login_required(DashboardView.as_view()), name='home'),
]
