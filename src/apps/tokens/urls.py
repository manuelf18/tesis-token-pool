from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (AdminPoolCreateView, AdminPoolListView,
                    AdminTokenTypeCreateView, AdminTokenTypeList,
                    PoolOffersCreateView, PoolOffersListView, PoolsDetailView,
                    PoolsListView, change_pool_status, create_transaction,
                    get_transactions_by_address, pay_withdraw_view)

app_name = 'tokens'

urlpatterns = [
    # client views
    path('pools', PoolsListView.as_view(), name='pools-list'),
    path('pools/<str:key>/offers/new', PoolOffersCreateView.as_view(), name='pools-offers-create'),
    path('pools/<str:key>/offers/list', PoolOffersListView.as_view(), name='pools-offers-list'),

    path('pools/<int:id>', PoolsDetailView.as_view(), name='pools-detail'),

    # admin views
    path('admin/token/list', login_required(AdminTokenTypeList.as_view()), name='admin-token-list'),
    path('admin/token/new', login_required(AdminTokenTypeCreateView.as_view()), name='admin-create-token-type'),
    path('admin/pool/list', login_required(AdminPoolListView.as_view()), name='admin-pool-list'),
    path('admin/pool/new', login_required(AdminPoolCreateView.as_view()), name='admin-create-pool'),

    # AJAX views
    path('pay/withdraw', pay_withdraw_view, name='pay-withdraw'),
    path('ajax/transactions/get', get_transactions_by_address, name='ajax-get-transactions'),
    path('ajax/transactions/create', create_transaction, name='ajax-create-transaction'),
    path('ajax/pool/changeStatus', login_required(change_pool_status), name='ajax-change-pool-status'),


]
