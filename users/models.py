from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.TextChoices):
    CLIENT = "client", "Клиент"
    WAREHOUSE = "warehouse_worker", "Складской рабочий"
    ADMIN = "admin", "Администратор"

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=UserRole.choices)