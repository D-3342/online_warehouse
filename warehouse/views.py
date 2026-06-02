from django.shortcuts import render
from .models import Product, Category

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    selected_category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')

    # Фильтр по категории
    if selected_category and selected_category != '':
        try:
            category_id = int(selected_category)
            products = products.filter(category_id=category_id)
        except (ValueError, TypeError):
            pass

    # Фильтр по поиску
    if search_query and search_query != '':
        products = products.filter(name__icontains=search_query)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }

    return render(request, 'pages/index.html', context)