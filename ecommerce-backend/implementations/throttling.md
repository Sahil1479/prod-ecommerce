We’ll use **DRF’s built-in throttling system** first (simple and quick), and then I’ll also show you how to extend it with **django-ratelimit** or Redis-based rate limiting for production-scale systems.

---

## 🔧 Step 1: Enable Throttling in Settings

In `settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "50/hour",   # anonymous users → 50 requests per hour
        "user": "200/hour",  # authenticated users → 200 requests per hour
    }
}
```

---

## 🔧 Step 2: Apply Per-View Throttling

If you want stricter limits on **specific endpoints**, add `throttle_classes` in the API view.

Example (`products/views.py`):

```python
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class ProductListView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
```

---

## 🔧 Step 3: Custom Throttle Class

If you want **different rate limits for different APIs**, subclass `UserRateThrottle`.

Example (`users/throttles.py`):

```python
from rest_framework.throttling import UserRateThrottle

class LoginRateThrottle(UserRateThrottle):
    scope = "login"
```

Now, add this scope to settings:

```python
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_RATES": {
        "anon": "50/hour",
        "user": "200/hour",
        "login": "5/minute",   # only 5 login attempts per minute
    }
}
```

Apply in Login view:

```python
from users.throttles import LoginRateThrottle

class LoginView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]
```

---

## 🔧 Step 4: Advanced (Optional) — Redis-based Rate Limiting

For distributed systems (multiple Django servers), DRF’s in-memory cache won’t be enough.
Use `django-ratelimit` or integrate Redis:

```bash
pip install django-ratelimit
```

Example usage:

```python
from ratelimit.decorators import ratelimit
from django.http import JsonResponse

@ratelimit(key="user_or_ip", rate="10/m", block=True)
def search_products(request):
    # 10 requests per minute allowed
    return JsonResponse({"message": "Search successful"})
```

---

## ✅ Example Test

### 1. Anonymous User

* Endpoint: `GET /api/v1/products/`
* Allowed: `50 requests/hour`

When exceeded → Response:

```json
{
  "detail": "Request was throttled. Expected available in 3600 seconds."
}
```

---