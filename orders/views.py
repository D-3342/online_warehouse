from decimal import Decimal

from django.shortcuts import render, redirect

from cart.models import CartItem
from catalog.models import Category, Product
from .models import Order, OrderItem


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    selected_category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')

    if selected_category:
        products = products.filter(category_id=selected_category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    popular_products = Product.objects.order_by('-view_count')[:8]

    return render(request, 'pages/index.html', {
        'products': products,
        'popular_products': popular_products,
        'selected_category': selected_category,
        'categories': categories,
        'search_query': search_query,
    })


def orders_page(request):
    orders = Order.objects.prefetch_related('items__product').all().order_by('-data_created')
    return render(request, 'pages/orders.html', {'orders': orders})


def checkout(request):
    if request.method != 'POST':
        return redirect('cart:cart_detail')

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        client = request.user
    else:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key).select_related('product')
        client = None

    if not cart_items.exists():
        return redirect('cart:cart_detail')

    order = Order.objects.create(
        client=client,
        status='new',
        total_price=Decimal('0.00')
    )

    for cart_item in cart_items:
        price = cart_item.product.get_discounted_price()
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.qty,
            price=price,
        )

    order.update_total()
    cart_items.delete()
    return redirect('orders:orders_page')