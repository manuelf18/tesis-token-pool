from django.contrib import admin
from .models import Pool
from .build import install


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'token_name', 'admin')
    list_filter = ['name', ]
    search_fields = ('token_name', 'name')
    actions_on_top = True
    actions_on_bottom = True

    def save_model(self, request, obj, form, change):
        if change is False:
            install(obj.name, obj.token_name)
        super().save_model(request, obj, form, change)
