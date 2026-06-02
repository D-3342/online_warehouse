# cart/views.py
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem
from catalog.models import Product


def get_cart(request):
    """Получить корзину пользователя"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return cart


def add_to_cart(request, product_id):
    """Добавить товар в корзину"""
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})