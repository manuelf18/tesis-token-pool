from django.urls import path

from .views import BuyerTemplateView, BuyTokenView, TestHelloWorldFormView

urlpatterns = [
    path('buyers', (BuyerTemplateView.as_view()), name='buyer-template'),
    path('buy/<int:pk>', (BuyTokenView.as_view()), name='buyer-create'),
    path('test', (TestHelloWorldFormView.as_view()), name='test-hello-world'),

]
