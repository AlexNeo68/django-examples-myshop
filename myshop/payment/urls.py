from django.urls import path

from payment.application.webhooks import stripe_webhook
from .views import payment_canceled, payment_completed, payment_process

app_name = 'payment'

urlpatterns = [
    path('process/', payment_process, name='process'),    
    path('completed/', payment_completed, name='completed'),    
    path('canceled/', payment_canceled, name='canceled'),    
    path('webhook/', stripe_webhook, name='stripe-webhook'),    
]
