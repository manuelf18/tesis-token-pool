from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (AdminPoolCreateView, AdminTokenTypeCreateView, PoolOffersCreateView, PoolOffersListView,
                    PoolsDetailView, PoolsListView, pay_withdraw_view)

app_name = 'tokens'

urlpatterns = [
    # client views
    path('pools', PoolsListView.as_view(), name='pools-list'),
    path('pools/<str:key>/offers/new', PoolOffersCreateView.as_view(), name='pools-offers-create'),
    path('pools/<str:key>/offers/list', PoolOffersListView.as_view(), name='pools-offers-list'),

    path('pools/<int:id>', PoolsDetailView.as_view(), name='pools-detail'),

    # admin views
    path('admin/pool/new', login_required(AdminPoolCreateView.as_view()), name='admin-create-pool'),
    path('admin/token-type/new', login_required(AdminTokenTypeCreateView.as_view()), name='admin-create-token-type'),


    # AJAX views
    path('pay/withdraw', pay_withdraw_view, name='pay-withdraw'),
]
