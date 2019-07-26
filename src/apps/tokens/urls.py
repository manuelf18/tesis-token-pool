from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (AdminPoolCreateView, AdminTokenTypeCreateView,
                    PoolsDetailView, PoolsListView, pay_deposit_view,
                    pay_withdraw_view)

app_name = 'tokens'

urlpatterns = [
    path('pools', PoolsListView.as_view(), name='pools-list'),
    path('pools/<int:id>', PoolsDetailView.as_view(), name='pools-detail'),

    # admin views
    path('admin/pool/new', login_required(AdminPoolCreateView.as_view()), name='admin-create-pool'),
    path('admin/token-type/new', login_required(AdminTokenTypeCreateView.as_view()), name='admin-create-token-type'),


    # AJAX views
    path('pay/deposit', pay_deposit_view, name='pay-deposit'),
    path('pay/withdraw', pay_withdraw_view, name='pay-withdraw'),
]
