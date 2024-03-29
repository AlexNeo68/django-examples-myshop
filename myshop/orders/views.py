from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from cart.cart import Cart
from shop.recommender import Recommender
from .tasks import order_created
from .forms import OrderCreateForm
from .models import Order, OrderItem
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            
            for item in cart:
                OrderItem.objects.create(order=order, 
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         )
            cart.clear()

            r = Recommender()
            cart_products = [item['product'] for item in cart]
            r.products_bought(cart_products)

            order_created.delay(order.id)

            # context = {
            #     'order': order
            # }
            # return render(request, 'orders/order/created.html', context)

            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    
    else:
        form = OrderCreateForm()
        context = {
            'form': form
        }
        return render(request, 'orders/order/create.html', context)
    
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order
    }
    return render(request, 'admin/orders/order/detail.html', context)


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order
    }
    html = render_to_string('orders/order/pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(
        settings.STATIC_ROOT / 'css/pdf.css'
    )])
    return response