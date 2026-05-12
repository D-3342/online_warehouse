from django.db import models
from users.models import User
from catalog.models import Product

class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    data_created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)