Perfect 👍 I’ll give you the **full final code** with:

1. `utils/circuit_breaker.py` (finalized with 5xx-only logic)
2. Example **APIView** using it (global breaker for all users).
3. If you want later, we can extend it per-user basis.

---

## 📂 `utils/circuit_breaker.py`

```python
# utils/circuit_breaker.py
import time
from threading import Lock


class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_time=30):
        """
        :param failure_threshold: Number of consecutive 5xx failures before opening circuit
        :param recovery_time: Time (seconds) to keep circuit open before allowing a retry
        """
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED -> OPEN -> HALF_OPEN
        self.lock = Lock()

    def _should_count_as_failure(self, status_code: int) -> bool:
        """Only count 5xx errors as circuit breaker failures."""
        return 500 <= status_code < 600

    def record_result(self, success: bool, status_code: int = None):
        """
        Record the result of an API call.
        :param success: True if call succeeded
        :param status_code: HTTP status code (used to decide if it counts toward breaker)
        """
        with self.lock:
            if success:
                self.failure_count = 0
                self.state = "CLOSED"
            else:
                if status_code is not None and not self._should_count_as_failure(status_code):
                    # Ignore 4xx, they don’t trip the breaker
                    return
                self.failure_count += 1
                self.last_failure_time = time.time()
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"

    def allow_request(self):
        """
        Check if a request should be allowed based on circuit state.
        """
        with self.lock:
            if self.state == "OPEN":
                if (time.time() - self.last_failure_time) > self.recovery_time:
                    # After cooldown, allow one test request
                    self.state = "HALF_OPEN"
                    return True
                return False
            return True
```

---

## 📂 Example APIView using Circuit Breaker

```python
# views.py
from django.http import JsonResponse
from rest_framework.views import APIView
import requests

from utils.circuit_breaker import CircuitBreaker

# Global circuit breaker instance for this service
breaker = CircuitBreaker(failure_threshold=3, recovery_time=20)


class ExternalAPIProxyView(APIView):
    """
    Proxy API that calls an external service with circuit breaker protection.
    """

    def get(self, request):
        # Step 1: Check if circuit is open
        if not breaker.allow_request():
            return JsonResponse(
                {"error": "Service temporarily unavailable (circuit open)"}, status=503
            )

        try:
            # Step 2: Make external request
            response = requests.get("https://httpbin.org/status/500", timeout=5)

            if 200 <= response.status_code < 300:
                # Success → reset breaker
                breaker.record_result(success=True)
                return JsonResponse({"data": response.json()})
            else:
                # Error response → count failure only for 5xx
                breaker.record_result(success=False, status_code=response.status_code)
                return JsonResponse(
                    {"error": "Upstream service error"},
                    status=response.status_code,
                )

        except requests.exceptions.RequestException:
            # Timeout or network failure = treat as 5xx
            breaker.record_result(success=False, status_code=503)
            return JsonResponse({"error": "Service unavailable"}, status=503)
```

---

## 📂 `urls.py`

```python
from django.urls import path
from .views import ExternalAPIProxyView

urlpatterns = [
    path("external/", ExternalAPIProxyView.as_view(), name="external-api"),
]
```

---

## ✅ Testing the Circuit Breaker

### 1. Call the API when external service is down

- Method: `GET`
- URL: `http://127.0.0.1:8000/api/v1/external/`

📌 First 3 failures (5xx responses) → API will try normally.
📌 On 4th failure → circuit opens → you get:

```json
{
  "error": "Service temporarily unavailable (circuit open)"
}
```

### 2. After recovery time (20s here)

Breaker goes **HALF_OPEN**, allows 1 request.

- If success → circuit closes.
- If fail → circuit stays open.

---
