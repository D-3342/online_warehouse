from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.CharField(max_length=300)
    expiration_date = models.DateField()
    image = models.ImageField(upload_to="products", blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def get_discounted_price(self):
        offer = getattr(self, "offer", None)
        if offer and offer.is_active:
            return (self.price * Decimal(100 - offer.discount_percent) / Decimal(100)).quantize(Decimal("0.01"))
        return self.price

    def __str__(self):
        return self.name


class Promotion(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    conditions = models.CharField(max_length=200)
    is_percent = models.BooleanField(default=True)
    discount = models.CharField(max_length=10)
    products = models.ManyToManyField(Product, related_name="promotions", blank=True)


class Offer(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="offer")
    title = models.CharField(max_length=200)
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    min_quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def discounted_price(self):
        return (self.product.price * Decimal(100 - self.discount_percent) / Decimal(100)).quantize(Decimal("0.01"))


class ProductView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_views")
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)