from django.urls import path
from .views import BuyerTemplateView

urlpatterns = [
    path('buyers', (BuyerTemplateView.as_view()), name='buyer-template'),
]
