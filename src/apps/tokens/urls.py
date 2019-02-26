from django.urls import path

from .views import BuyerTemplateView, BuyTokenView, GetTokenView

urlpatterns = [
    path('buy/list', (BuyerTemplateView.as_view()), name='buyer-template'),
    path('buy/<int:pk>', (BuyTokenView.as_view()), name='buyer-create'),
    path('get/<int:pk>', (GetTokenView.as_view()), name='buyer-retrieve'),
]
