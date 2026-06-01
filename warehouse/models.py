from django.db import models
from catalog.models import Product, Category
from suppliers.models import Supplier

class ProductBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="batches")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="batches")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="batches")
    received_date = models.DateField()
    expiration_date = models.DateField()
    quantity = models.IntegerField()