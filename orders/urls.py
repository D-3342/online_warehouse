# orders/urls.py
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render
from . import views

from orders.views import orders_page

app_name = 'orders'

urlpatterns = [
    path('', orders_page, name='orders_page'),

]