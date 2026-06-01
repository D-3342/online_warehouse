from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'  # Пространство имен для users

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]