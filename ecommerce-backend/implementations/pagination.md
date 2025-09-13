
---

# ⚡ Pagination in DRF

### 1. Why Pagination?

When you query large tables (e.g., products, orders, reviews), returning everything at once is inefficient.
Pagination:

* Splits results into pages.
* Reduces payload size.
* Improves performance.
* Supports infinite scroll or "Load more" in frontend.

---

### 2. DRF Pagination Options

DRF provides multiple styles:

* **PageNumberPagination** → `?page=2` (classic pages).
* **LimitOffsetPagination** → `?limit=10&offset=20`.
* **CursorPagination** → good for very large datasets (uses encoded cursor).

---

### 3. Settings (`settings.py`)

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,  # default items per page
}
```

---

### 4. Example in Products API

Update `ProductListAPIView`:

```python
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"  # client can override
    max_page_size = 100


class ProductListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        products = Product.objects.all().order_by("-created_at")
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
```

---

### 5. Example Response

Request:

```
GET /api/v1/products/?page=2&page_size=5
```

Response:

```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/v1/products/?page=3&page_size=5",
  "previous": "http://127.0.0.1:8000/api/v1/products/?page=1&page_size=5",
  "results": [
    {
      "id": 6,
      "name": "Laptop",
      "price": 1200,
      "stock": 5,
      "seller": 2
    },
    ...
  ]
}
```
