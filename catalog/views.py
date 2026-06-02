# catalog/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def dish_list(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    search_query = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '')
    sort = request.GET.get('sort', 'name')

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    if category_id and category_id.isdigit():
        products = products.filter(category_id=int(category_id))

    allowed_sort_fields = {'name', '-name', 'price', '-price'}
    if sort in allowed_sort_fields:
        products = products.order_by(sort)
    else:
        sort = 'name'
        products = products.order_by(sort)

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_sort': sort,
    }
    return render(request, 'pages/products/catalog.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    return render(request, 'pages/products/detail.html', {'product': product})