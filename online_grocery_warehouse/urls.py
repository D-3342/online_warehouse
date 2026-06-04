from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from online_grocery_warehouse import settings
import orders.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', orders.views.home, name='home'),
    path('orders/', include('orders.urls')),
    path('accounts/', include('users.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', include(('catalog.urls', 'catalog'), namespace='catalog')),
    path('cart/', include('cart.urls')),
    path('warehouse/', include(('warehouse.urls', 'warehouse'), namespace='warehouse')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)