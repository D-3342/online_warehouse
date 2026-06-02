from django.shortcuts import render

from catalog.models import Category
from .models import Product, Order


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    selected_category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')

    if selected_category:
        products = products.filter(category_id=selected_category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'pages/index.html', {
        'products': products,
        'selected_category': selected_category,
        'categories': categories,
        'search_query': search_query,
    })


def orders_page(request):
    orders = Order.objects.prefetch_related('items__product').all().order_by('-data_created')
    return render(request, 'pages/orders.html', {'orders': orders})
