from django.db import models
from users.models import User 
from django.core.validators import MaxValueValidator

# Indexing imports
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

# -----------------------------
# Category Model (with self relation for subcategories)
# -----------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# -----------------------------
# Product Model
# -----------------------------
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    search_vector = SearchVectorField(null=True, blank=True)  # For full-text search

    class Meta:
        indexes = [
            models.Index(fields=["price"]),
            GinIndex(fields=["search_vector"]),
        ]

    def __str__(self):
        return self.name
    
# -----------------------------
# Product Subscription Model
# -----------------------------
class ProductSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} subscribed to {self.product.name}"


# -----------------------------
# Review Model
# -----------------------------
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], validators=[MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user') # One review per user per product
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"