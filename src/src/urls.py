from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include(('apps.profiles.urls', 'profiles'))),
    path('tokens/', include(('apps.tokens.urls', 'tokens'))),
]
