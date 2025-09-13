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

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
