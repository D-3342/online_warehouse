from django.db import models
from django.conf import settings
from catalog.models import Product

class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    data_created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calculate_total(self):
        """Вычисляет общую сумму из OrderItem"""
        total = sum(item.quantity * item.price for item in self.items.all())
        return total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Сначала сохраняем (чтобы получил id)
        # Потом считаем сумму и сохраняем снова
        self.total_price = self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ {self.id} — {self.total_price} ₽"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Цена берётся из продукта
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def get_subtotal(self):
        return self.quantity * self.price