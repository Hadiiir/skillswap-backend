from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment History
    path('history/', views.PaymentHistoryView.as_view(), name='history'),
    
    # Payment Gateways
    path('stripe/', views.StripePaymentView.as_view(), name='stripe'),
    path('paypal/', views.PayPalPaymentView.as_view(), name='paypal'),
    path('paymob/', views.PaymobPaymentView.as_view(), name='paymob'),
]
