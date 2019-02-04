from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeView, LoginView, SignUpView

urlpatterns = [
    path('', (HomeView.as_view()), name='home'),
    path('login', (LoginView.as_view()), name='login'),
    path('logout', (LogoutView.as_view(template_name='index.pug')), name='logout'),
    path('signup', (SignUpView.as_view()), name='signup')
]
