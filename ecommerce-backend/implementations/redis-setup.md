---
---

# 🔹 1. Install Redis on macOS

```bash
brew install redis
```

---

# 🔹 2. Start Redis Server

Start it as a background service (recommended):

```bash
brew services start redis
```

Or run it manually in a terminal:

```bash
redis-server
```

---

# 🔹 3. Verify Redis is Running

```bash
redis-cli ping
```

If it replies with:

```
PONG
```

✅ Redis is running.

---

# 🔹 4. Install Redis Python Client

Inside your Django project’s **virtual environment**:

```bash
pip install redis
```

---

# 🔹 5. Install Django Redis Cache Backend

```bash
pip install django-redis
```

---

# 🔹 6. Configure Django to Use Redis

In your project’s **`settings.py`**, add Redis as a cache backend:

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # db index 1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

👉 Explanation:

- `127.0.0.1` → Local Redis server
- `6379` → Default Redis port
- `/1` → Redis database index (you can use 0–15)

---

# 🔹 7. Use Redis for Sessions (Optional)

If you want Django sessions in Redis:

```python
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

---

# 🔹 8. Test Redis in Django Shell

Run:

```bash
python manage.py shell
```

Then:

```python
from django.core.cache import cache
cache.set("foo", "bar", timeout=60)
print(cache.get("foo"))
```

👉 You should see `"bar"`.

---

# 🔹 9. Stop Redis (when not needed)

If running as service:

```bash
brew services stop redis
```

If running manually:

```bash
pkill redis-server
```

---
