from django.urls import path

from .views import HomeView, LoginView, SignUpView

urlpatterns = [
    path('', (HomeView.as_view()), name='home'),
    path('login', (LoginView.as_view()), name='login'),
    path('signup', (SignUpView.as_view()), name='signup')
]
