from django.contrib import admin
from django.core.exceptions import MultipleObjectsReturned

from .contracts import PoolContract
from .models import Network, Pool, TokenType, Transaction


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'token_type', 'admin')
    list_filter = ['name', ]
    search_fields = ('name', )
    actions_on_top = True
    actions_on_bottom = True


@admin.register(TokenType)
class TokenTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ['name', ]
    search_fields = ('name', )
    actions_on_top = True
    actions_on_bottom = True


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ('url', 'port', 'connected')
    list_filter = ['connected', 'url', 'port', ]
    actions_on_top = True
    actions_on_bottom = True

    def save_model(self, request, obj, form, change):
        if change is True and obj.active is True:
            try:
                prev_active = Network.objects.get(connected=True)
                prev_active.connected = False
                prev_active.save(update_fields=['connected'])
            except (Network.DoesNotExist):
                # Fail Silently if there is no active network
                pass
            except (MultipleObjectsReturned):
                multiple_actives = Network.objects.filter(connected=True)
                multiple_actives.update(connected=False)

        super().save_model(request, obj, form, change)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'address', 'transaction_type', 'amount', 'value', )
    actions_on_top = True
    actions_on_bottom = True
