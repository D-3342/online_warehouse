# orders/urls.py
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render

# Временные вьюхи для проверки
def order_list(request):
    return HttpResponse("Список заказов - в разработке")

def order_detail(request, pk):
    return HttpResponse(f"Детали заказа #{pk} - в разработке")

def create_order(request):
    return HttpResponse("Создание заказа - в разработке")

app_name = 'orders'

urlpatterns = [
    path('', order_list, name='order_list'),
    path('<int:pk>/', order_detail, name='order_detail'),
    path('create/', create_order, name='create_order'),
]