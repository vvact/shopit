from django.urls import path
from .views import CODPaymentView

urlpatterns = [
    path('cod/', CODPaymentView.as_view(), name='cod-payment'),
]
