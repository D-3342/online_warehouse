from django.shortcuts import render
from .models import Product, Category

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    selected_category = request.GET.get('category')

    if selected_category:
        products = products.filter(category_id=selected_category)

    return render(request, 'pages/index.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }),