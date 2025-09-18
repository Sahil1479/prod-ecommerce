
---

# 📌 Implementation: Product Filtering + Search (Django + Postgres)

---

## 🔹 1. Install dependencies

We’ll use **django-filter** for filters:

```bash
pip install django-filter
```
## Add Postgres Extensions
```
Inside psql:
psql -U <username> -d <your_database>
CREATE EXTENSION IF NOT EXISTS pg_trgm;   -- for trigram similarity
CREATE EXTENSION IF NOT EXISTS unaccent; -- optional, for accent-insensitive search

\dx
You should see pg_trgm in the list of installed extensions.

```

Add to `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "django_filters",
]
```

---

## 🔹 2. Update Product Model (ensure `search_vector` exists)

```python
# products/models.py
from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["category"]),
            GinIndex(fields=["search_vector"]),
        ]

    def __str__(self):
        return self.name
```

---

## 🔹 3. Keep `search_vector` Updated

```python
# products/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import Product

@receiver(post_save, sender=Product)
def update_search_vector(sender, instance, **kwargs):
    Product.objects.filter(id=instance.id).update(
        search_vector=(
            SearchVector("name", weight="A") +
            SearchVector("description", weight="B")
        )
    )
```

Enable signals in `apps.py`:

```python
# products/apps.py
from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        import products.signals
```

---

## 🔹 4. Filters Setup

```python
# products/filters.py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.CharFilter(field_name="category", lookup_expr="iexact")

    class Meta:
        model = Product
        fields = ["min_price", "max_price", "category"]
```

---

## 🔹 5. Serializer

```python
# products/api/v1/serializers.py
from rest_framework import serializers
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "category"]
```

---

## 🔹 6. Views (Search + Filter)

```python
# products/api/v1/views.py
from rest_framework import generics
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from products.models import Product
from .serializers import ProductSerializer
from products.filters import ProductFilter

class ProductSearchAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ["price", "name"]

    def get_queryset(self):
        queryset = Product.objects.all()
        query = self.request.query_params.get("q")

        if query:
            search_query = SearchQuery(query)
            queryset = queryset.annotate(
                rank=SearchRank("search_vector", search_query),
                similarity=TrigramSimilarity("name", query),
            ).filter(search_vector=search_query).order_by("-rank", "-similarity")

        return queryset
```

---

## 🔹 7. URLs

```python
# products/api/v1/urls.py
from django.urls import path
from .views import ProductSearchAPIView

urlpatterns = [
    path("search/", ProductSearchAPIView.as_view(), name="product-search"),
]
```

Include in main `urls.py`:

```python
path("api/v1/products/", include("products.api.v1.urls")),
```

---

## 🔹 8. Example Queries

### ✅ Filter by category:

```
GET /api/v1/products/search/?category=mobile
```

### ✅ Price range:

```
GET /api/v1/products/search/?min_price=500&max_price=1000
```

### ✅ Search text:

```
GET /api/v1/products/search/?q=iphone
```

### ✅ Combined:

```
GET /api/v1/products/search/?q=iphone&min_price=50000&category=mobile&ordering=price
```

---

## 🔹 9. Sample Response

```json
[
  {
    "id": 1,
    "name": "iPhone 15",
    "description": "Latest Apple iPhone with A17 chip",
    "price": "79999.00",
    "category": "mobile"
  },
  {
    "id": 2,
    "name": "iPhone 14",
    "description": "Previous generation iPhone",
    "price": "69999.00",
    "category": "mobile"
  }
]
```

---

✅ Now you have **full-text search + fuzzy search + filtering + ordering** in one clean API 🎯.

Do you want me to also add **pagination + DRF schema docs (Swagger/Redoc)** so that the API is fully production-ready?
