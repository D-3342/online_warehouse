from django.contrib import admin
from django.urls import path

from warehouse.views import *

from django.urls import path
from catalog.views import *

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]
