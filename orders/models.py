from django.db import models
from django.conf import settings
from catalog.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменён'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    data_created = models.DateField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def calculate_total(self):
        total = sum(item.get_subtotal() for item in self.items.all())
        return total

    def update_total(self):
        self.total_price = self.calculate_total()
        super(Order, self).save(update_fields=['total_price'])

    def __str__(self):
        return f"Заказ {self.id} — {self.total_price} ₽"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def get_subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"