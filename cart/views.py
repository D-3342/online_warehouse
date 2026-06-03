from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from catalog.models import Product


def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('catalog:product_list')

    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('qty', 1))

    if qty < 1:
        qty = 1
    if qty > product.quantity:
        qty = product.quantity

    cart = request.session.get('cart', {})
    key = str(product.id)
    cart[key] = cart.get(key, 0) + qty

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=ids)

    items = []
    total = Decimal('0.00')

    for product in products:
        qty = cart.get(str(product.id), 0)
        item_total = product.price * qty
        total += item_total
        items.append({
            'product': product,
            'qty': qty,
            'item_total': item_total,
        })

    return render(request, 'pages/cart/cart.html', {
        'items': items,
        'total': total,
    })