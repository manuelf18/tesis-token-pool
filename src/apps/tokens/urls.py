from django.urls import path

from .views import (BuyerTemplateView, BuyTokenView, GetTokenView, StatusView,
                    PoolsListView, PoolsDetailView, pay_view)

urlpatterns = [
    path('pools', PoolsListView.as_view(), name='pools-list'),
    path('pools/<int:id>', PoolsDetailView.as_view(), name='pools-detail'),
    path('buy/list', (BuyerTemplateView.as_view()), name='buyer-template'),
    path('buy/<int:pk>', (BuyTokenView.as_view()), name='buyer-create'),
    path('get/<int:pk>', (GetTokenView.as_view()), name='buyer-retrieve'),
    path('status', (StatusView.as_view()), name='status'),
    path('pay', pay_view, name='pay'),
]
