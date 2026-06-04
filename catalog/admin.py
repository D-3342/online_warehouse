from django.contrib import admin
from .models import Category, Product, Offer


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


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'discount_percent', 'min_quantity', 'is_active']
    list_filter = ['is_active', 'discount_percent']
    search_fields = ['title', 'product__name']