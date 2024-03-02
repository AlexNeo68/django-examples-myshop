from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import admin_order_detail, admin_order_pdf, order_create

app_name = 'orders'

urlpatterns = [
    path(_('create/'), order_create, name='order_create'),
    path('admin/orders/<int:order_id>/', admin_order_detail, name='admin_order_detail'),
    path('admin/orders/<int:order_id>/pdf/', admin_order_pdf, name='admin_order_pdf'),
]
