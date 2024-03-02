from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import payment_canceled, payment_completed, payment_process

app_name = 'payment'

urlpatterns = [
    path(_('process/'), payment_process, name='process'),    
    path(_('completed/'), payment_completed, name='completed'),    
    path(_('canceled/'), payment_canceled, name='canceled'),      
]
