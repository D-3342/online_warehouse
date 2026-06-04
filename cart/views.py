from decimal import Decimal

from django.shortcuts import render, redirect
from .models import CartItem


def cart_detail(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).select_related('product', 'product__offer')
    else:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key).select_related('product', 'product__offer')

    items = []
    total = Decimal('0.00')

    for item in cart_items:
        product = item.product
        offer = getattr(product, 'offer', None)

        old_price = product.price
        old_total = old_price * item.qty

        show_discount = bool(offer and offer.is_active and item.qty >= offer.min_quantity)

        if show_discount:
            discounted_price = (product.price * Decimal(100 - offer.discount_percent) / Decimal(100)).quantize(Decimal('0.01'))
            item_total = discounted_price * item.qty
        else:
            discounted_price = old_price
            item_total = old_total

        items.append({
            'product': product,
            'qty': item.qty,
            'old_price': old_price,
            'discounted_price': discounted_price,
            'old_total': old_total,
            'item_total': item_total,
            'show_discount': show_discount,
            'min_quantity': offer.min_quantity if offer else None,
            'discount_percent': offer.discount_percent if offer else None,
        })
        total += item_total

    return render(request, 'pages/cart/cart.html', {
        'items': items,
        'total': total,
    })


def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('qty', 1))

        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product_id=product_id)
        else:
            if not request.session.session_key:
                request.session.create()
            cart_item, created = CartItem.objects.get_or_create(session_key=request.session.session_key, product_id=product_id)

        if not created:
            cart_item.qty += quantity
        else:
            cart_item.qty = quantity

        cart_item.save()
        return redirect('cart:cart_detail')

    return redirect('cart:cart_detail')


def edit_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('qty', 1))

        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
        else:
            cart_item = CartItem.objects.filter(session_key=request.session.session_key, product_id=product_id).first()

        if cart_item and quantity > 0:
            cart_item.qty = quantity
            cart_item.save()

        return redirect('cart:cart_detail')

    return redirect('cart:cart_detail')


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
        else:
            cart_item = CartItem.objects.filter(session_key=request.session.session_key, product_id=product_id).first()

        if cart_item:
            cart_item.delete()

        return redirect('cart:cart_detail')

    return redirect('cart:cart_detail')