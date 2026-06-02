import orders.views
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from catalog.views import dish_list, product_detail
from online_grocery_warehouse import settings
from users.views import register_view, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', orders.views.home, name='home'),
    path('orders/', include('orders.urls')),  # orders приложение
    path('accounts/', include('users.urls')),  # стандартные URL для аутентификации
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', include(('catalog.urls', 'catalog'), namespace='catalog')),
    path('orders/', orders.views.orders_page, name='orders'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)