from django.db import models

class Supplier(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"