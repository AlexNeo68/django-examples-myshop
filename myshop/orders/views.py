from django.shortcuts import render

from cart.cart import Cart
from .tasks import order_created
from .forms import OrderCreateForm
from .models import OrderItem

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, 
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'],
                                         )
            cart.clear()

            order_created.delay(order.id)

            context = {
                'order': order
            }
            return render(request, 'orders/order/created.html', context)
    
    else:
        form = OrderCreateForm()
        context = {
            'form': form
        }
        return render(request, 'orders/order/create.html', context)