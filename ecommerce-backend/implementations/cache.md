
Since want to stick with **Django’s provided caching backends** instead of installing Redis, let’s use **Memcached** (fast + widely used) or **LocMemCache** (good for development).

---

# ⚡ Caching with Django’s Built-in Backends

### 1. Install Memcached (recommended for production)

* **Ubuntu/Debian**

  ```bash
  sudo apt install memcached libmemcached-tools
  ```
* **Mac (Homebrew)**

  ```bash
  brew install memcached
  brew services start memcached
  ```

Python bindings:

```bash
pip install python-memcached
```

---

### 2. Update `settings.py`

Choose **Memcached** (for production) OR **LocMemCache** (for dev/testing).

#### Option A: Memcached

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

CACHE_TTL = 60 * 5  # 5 minutes
```

#### Option B: LocMemCache (simple in-memory, per process)

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

CACHE_TTL = 60 * 5
```

---

### 3. Add Caching in Views (Same as Redis approach)

Example for **Product APIs**:

```python
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ProductListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(60 * 2))  # 2 minutes caching at view level
    def get(self, request):
        products = cache.get("all_products")
        if not products:
            products = Product.objects.all().order_by("-created_at")
            cache.set("all_products", products, timeout=60 * 2)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

Example for **Product Detail**:

```python
class ProductDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        cache_key = f"product_{pk}"
        product = cache.get(cache_key)
        if not product:
            product = get_object_or_404(Product, pk=pk)
            cache.set(cache_key, product, timeout=60 * 5)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
```

---

### 4. Cache Invalidation (important!)

Whenever data changes:

```python
def post(self, request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(seller=request.user)
        cache.delete("all_products")   # clear product list cache
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

Similarly, invalidate `product_{pk}`, `category_{pk}`, `reviews_product_{id}` etc. on update/delete.

---

### 5. Summary

* ✅ Use **Memcached** in production (`django.core.cache.backends.memcached.MemcachedCache`).
* ✅ Use **LocMemCache** for dev/testing (no extra install).
* ✅ Add `cache_page` + manual `cache.get/set` for queries.
* ✅ Invalidate cache after create/update/delete.

---