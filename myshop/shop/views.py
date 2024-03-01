from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from .recommender import Recommender

from .models import Category, Product

def product_list(request, category_slug=None):
    
    categories = Category.objects.all()
    

    if category_slug:
        category = Category.objects.filter(slug=category_slug)
        products = Product.objects.filter(available=True, category=category)
    else:
        products = Product.objects.filter(available=True)
        category = None

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }

    return render(request, 'shop/product/list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'recommended_products': recommended_products,
    }
    return render(request, 'shop/product/detail.html', context)