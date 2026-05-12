from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'data_created', 'status', 'total_price']
    list_filter = ['status', 'data_created']
    search_fields = ['client__email', 'client__first_name']
    inlines = [OrderItemInline]
    readonly_fields = ['total_price']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']