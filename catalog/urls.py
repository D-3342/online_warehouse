from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.dish_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
]