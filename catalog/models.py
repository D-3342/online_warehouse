from django.db import models
from django.db.models import ImageField


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
    image = ImageField(upload_to="products", blank=True)

    def __str__(self):
        return self.name

class Promotion(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    conditions = models.CharField(max_length=200)
    is_percent = models.BooleanField(default=True)
    discount = models.CharField(max_length=10)
    products = models.ManyToManyField(Product, related_name="promotions", blank=True)