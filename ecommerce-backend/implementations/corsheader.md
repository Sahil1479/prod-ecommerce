This is usually about **CORS (Cross-Origin Resource Sharing)**, because React runs on a different origin (e.g., `http://localhost:3000`) than Django (`http://localhost:8000`).

Here’s how you configure it:

---

## 🔹 1. Install Django CORS Headers

In your Django backend (virtualenv):

```bash
pip install django-cors-headers
```

---

## 🔹 2. Add to `INSTALLED_APPS`

In `settings.py`:

```python
INSTALLED_APPS = [
    ...,
    "corsheaders",
]
```

---

## 🔹 3. Add Middleware

Put it **at the top** of `MIDDLEWARE` (just after `SecurityMiddleware`):

```python
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...
]
```

---

## 🔹 4. Allow React frontend origin

For **development** (React running on `http://localhost:3000`):

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

---

## 🔹 5. (Optional) Allow all origins (only for testing!)

```python
CORS_ALLOW_ALL_ORIGINS = True
```

⚠️ Not recommended for production — always whitelist your frontend domain(s).

---

## 🔹 6. Handling Cookies / Authentication (if needed)

If your React app uses **JWT** or **session cookies**, add:

```python
CORS_ALLOW_CREDENTIALS = True
```

Then in your React `fetch` or `axios` calls, include:

```js
fetch("http://localhost:8000/api/", {
  credentials: "include",
});
```

---
