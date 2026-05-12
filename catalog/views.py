from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Product

def index(request):
    products = [
        {
            "name": "Молоко 2.5%",
            "price": 79.50,
            "description": "Пастеризованное молоко свежего вкуса.",
        },
        {
            "name": "Сыр Гауда",
            "price": 650.00,
            "description": "Полутвердый сыр для бутербродов и закусок.",
        },
    ]
    return render(request, "pages/index.html", {"products": products})

def product_list(request):
    search_query = request.GET.get('search', '').strip()
    products = Product.objects.select_related('category').all()

    if search_query:
        products = products.filter(
            name__icontains=search_query
        ) | products.filter(
            description__icontains=search_query
        ) | products.filter(
            category__name__icontains=search_query
        )

    context = {
        'products': products.distinct(),
        'search_query': search_query,
    }
    return render(request, 'pages/products/list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    return render(request, 'pages/products/detail.html', {'product': product})