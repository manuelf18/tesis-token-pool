from django.contrib import admin
from apps.tokens.models import Pool


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'token_name', 'admin')
    list_filter = ['name', ]
    search_fields = ('token_name', 'name')
    actions_on_top = True
    actions_on_bottom = True
