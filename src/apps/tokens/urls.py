from django.urls import path

from .views import (BuyerTemplateView, BuyTokenView, GetTokenView,
                    PoolsDetailView, PoolsListView, StatusView,
                    pay_deposit_view, pay_withdraw_view)

urlpatterns = [
    path('pools', PoolsListView.as_view(), name='pools-list'),
    path('pools/<int:id>', PoolsDetailView.as_view(), name='pools-detail'),
    path('buy/list', (BuyerTemplateView.as_view()), name='buyer-template'),
    path('buy/<int:pk>', (BuyTokenView.as_view()), name='buyer-create'),
    path('get/<int:pk>', (GetTokenView.as_view()), name='buyer-retrieve'),
    path('status', (StatusView.as_view()), name='status'),



    # AJAX views
    path('pay/deposit', pay_deposit_view, name='pay-deposit'),
    path('pay/withdraw', pay_withdraw_view, name='pay-withdraw'),
]
