# catalog/urls.py
from django.urls import path
from . import views
from django.shortcuts import render
from .models import Product, Category

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='home'),
    path('products/', views.dish_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
]

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    selected_category = request.GET.get('category')

    if selected_category:
        products = products.filter(category_id=selected_category)

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    })