from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------
# User Model with Roles
# -----------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('seller', 'seller'),
        ('customer', 'customer'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.username} ({self.role})"
