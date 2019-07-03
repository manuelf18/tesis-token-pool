from django.urls import path

from .views import (BuyerTemplateView, BuyTokenView, GetTokenView, StatusView,
                    TokensListView, pay_view)

urlpatterns = [
    path('', TokensListView.as_view(), name='tokens-list'),
    path('buy/list', (BuyerTemplateView.as_view()), name='buyer-template'),
    path('buy/<int:pk>', (BuyTokenView.as_view()), name='buyer-create'),
    path('get/<int:pk>', (GetTokenView.as_view()), name='buyer-retrieve'),
    path('status', (StatusView.as_view()), name='status'),
    path('pay', pay_view, name='pay'),
]
