from django.contrib import admin
from .models import Category, Product, Promotion


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'products_count']
    search_fields = ['name']
    ordering = ['name']

    def products_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'quantity', 'expiration_date']
    list_filter = ['category', 'expiration_date']
    search_fields = ['name', 'brand', 'description']
    ordering = ['name']
    list_editable = ['price', 'quantity']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'conditions', 'is_percent', 'discount']
    list_filter = ['is_percent', 'start_date', 'end_date']
    filter_horizontal = ['products']