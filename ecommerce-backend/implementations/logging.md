Observability = **being able to understand what’s happening inside your system in real-time**.
It’s not just about errors — it includes **logs, metrics, traces**.

Here, we’ll focus on **logging** first.

---

# 🔎 Why Logging?

* **Debugging:** See what happened before a crash.
* **Audit trail:** Track who did what (e.g., user actions).
* **Performance monitoring:** Log slow queries, long response times.
* **Security:** Detect brute-force login attempts, suspicious activity.
* **Integration:** Forward logs to tools like ELK, Datadog, Splunk, Grafana Loki.

---

Perfect! Let’s create a **complete, clean, production-ready logging setup** for Django + DRF using a **single namespace (`ecommerce`)**, JSON logs, request ID, event name, timestamp, and payload. I’ll include:

* `settings.py` logging config
* Logging helper function
* Example view using it
* Instructions to test locally

---

# 1️⃣ Install Dependencies

```bash
pip install django-request-id
```

* This will generate unique request IDs automatically.

---

# 2️⃣ `settings.py` Logging Configuration

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

MIDDLEWARE = [
    "django_request_id.middleware.RequestIDMiddleware",  # must be early
    # ... other middleware
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "json": {
            "format": (
                '{{"timestamp": "{asctime}", "level": "{levelname}", '
                '"logger": "{name}", "request_id": "{request_id}", '
                '"event": "{event}", "payload": "{payload}"}}'
            ),
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "app.json.log",
            "formatter": "json",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "errors.json.log",
            "formatter": "json",
            "level": "ERROR",
        },
    },

    "loggers": {
        "ecommerce": {  # single project namespace
            "handlers": ["console", "file", "error_file"],
            "level": "INFO",  # INFO in prod, DEBUG for dev
            "propagate": False,
        },
    },
}
```

---

# 3️⃣ Logging Helper (`ecommerce/logging_helper.py`)

```python
import logging
from django_request_id.middleware import current_request_id

logger = logging.getLogger("ecommerce")

def log_event(event_name, payload=None, level="INFO"):
    """
    Logs an event in JSON format with request_id, event name, payload, timestamp.
    """
    extra = {
        "request_id": current_request_id(),
        "event": event_name,
        "payload": payload if payload else {},
    }

    if level.upper() == "INFO":
        logger.info(event_name, extra=extra)
    elif level.upper() == "ERROR":
        logger.error(event_name, extra=extra, exc_info=True)
    else:
        logger.log(getattr(logging, level.upper(), logging.INFO), event_name, extra=extra)
```

---

# 4️⃣ Example View (`products/views.py`)

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from ecommerce.logging_helper import log_event

class ProductListView(APIView):
    def get(self, request):
        log_event("fetch_products_start", payload={"path": request.path}, level="INFO")

        try:
            products = Product.objects.all()
            log_event(
                "fetch_products_success",
                payload={"count": products.count()},
                level="INFO"
            )
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            log_event("fetch_products_error", payload={"error": str(e)}, level="ERROR")
            return Response({"error": "Server error"}, status=500)

    def post(self, request):
        payload = request.data
        log_event("create_product_start", payload=payload, level="INFO")
        try:
            serializer = ProductSerializer(data=payload)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            log_event("create_product_success", payload=serializer.data, level="INFO")
            return Response(serializer.data)
        except Exception as e:
            log_event("create_product_error", payload={"error": str(e)}, level="ERROR")
            return Response({"error": "Server error"}, status=500)
```

---

# 5️⃣ Testing Locally

1. Start Django server:

```bash
python manage.py runserver
```

2. Make GET request:

```bash
curl http://127.0.0.1:8000/api/products/
```

3. Make POST request:

```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "stock": 10, "price": 50000}'
```

4. Check logs:

* **Console:** you’ll see JSON logs
* **File logs:**

  * `logs/app.json.log` → all INFO+
  * `logs/errors.json.log` → only ERRORs

**Sample log line:**

```json
{
  "timestamp": "2025-09-14 21:30:12",
  "level": "INFO",
  "logger": "ecommerce.products.views",
  "request_id": "d3b7e8f4-2f4a-4e3b-a123-9c8d7f1c5678",
  "event": "fetch_products_success",
  "payload": {"count": 5}
}
```

---

# ✅ Summary

* Single namespace `ecommerce` → simpler configuration
* JSON logs with **timestamp, event, payload, request ID**
* INFO/ERROR levels supported
* Logging helper for standardized usage in views and tasks
* Works with **django-request-id** for correlation ID

---

