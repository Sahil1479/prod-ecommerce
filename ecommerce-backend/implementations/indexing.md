
---

# 📌 Indexing & Full-Text Search in Django (with Postgres)

---

## 🔹 1. Setup

### 1.1 Ensure Postgres & Django Support

* Use PostgreSQL ≥ 12 (better FTS performance).
* Install psycopg driver:

```bash
pip install psycopg2-binary
```

### 1.2 Add Postgres Extensions

Inside `psql`:

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;   -- for trigram similarity
CREATE EXTENSION IF NOT EXISTS unaccent; -- optional, for accent-insensitive search
```

Update `settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ecommerce",
        "USER": "postgres",
        "PASSWORD": "yourpassword",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

---

## 🔹 2. Types of Indexing in Django

### 2.1 B-Tree Index (Default)

Best for **sorting, filtering, ranges**.

```python
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=["price"]),   # single-column index
            models.Index(fields=["category"]), # faster category filter
            models.Index(fields=["price", "category"]), # composite index
        ]
```

✅ Useful for:

* `Product.objects.filter(price__lte=500)`
* `Product.objects.filter(price=500, category="mobile")`

---

### 2.2 Full-Text Search (SearchVector + GIN)

For **searching text at scale**.

```python
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    search_vector = SearchVectorField(null=True)  # stores tokens

    class Meta:
        indexes = [
            GinIndex(fields=["search_vector"]),  # super-fast FTS
        ]
```

---

## 🔹 3. Implementation

### 3.1 Update `search_vector` on Save

```python
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

---

### 3.2 Searching Products

```python
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import Product

query = SearchQuery("iphone")
products = Product.objects.annotate(
    rank=SearchRank("search_vector", query)
).filter(search_vector=query).order_by("-rank")
```

✅ Orders results by **relevance**.

---

### 3.3 Trigram Similarity (Fuzzy Search)

```python
from django.contrib.postgres.search import TrigramSimilarity
Product.objects.annotate(
    similarity=TrigramSimilarity("name", "iphone")
).filter(similarity__gt=0.3).order_by("-similarity")
```

✅ Useful for typos:
Searching `"iphnoe"` → returns `"iPhone"`.

---

## 🔹 4. Testing the Setup

### 4.1 Check Table Indexes

```sql
\d products_product;
```

You should see:

* `btree (price)`
* `btree (category)`
* `gin (search_vector)`

### 4.2 Run Search

**Test API** (example `GET /api/v1/products/search/?q=iphone`):

```json
[
  {
    "id": 1,
    "name": "iPhone 15",
    "description": "Latest Apple iPhone with A17 chip",
    "rank": 0.92
  },
  {
    "id": 2,
    "name": "iPhone 14",
    "description": "Previous gen iPhone",
    "rank": 0.81
  }
]
```

✅ Search is **fast** even with millions of rows because:

* B-Tree handles numeric/range filters.
* GIN handles full-text search.

---

## 🔹 5. Summary

* **B-Tree Index** → Fast filtering (`price`, `category`).
* **GIN Index + SearchVector** → Full-text search (tokenized).
* **Trigram Search** → Fuzzy/typo handling.
* **Composite Index** → Multi-field filters.
* **Signal Updates** → Keep search vectors synced automatically.
* **ElasticSearch** → Only needed if queries are extremely complex or require multi-language/analytics.

---

👉 This way, you get **production-grade indexing + search optimizations inside Django itself**, without needing ElasticSearch unless your use case is very advanced.