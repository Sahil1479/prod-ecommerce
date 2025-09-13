
---

## 🔑 Why Logout/Token Blacklist is Needed

With JWT:

* When a user logs in, they get a **refresh token** and **access token**.
* Even if the user logs out from frontend, the **refresh token is still valid** until it expires.
* This means if an attacker gets hold of the refresh token, they can still generate new access tokens.
* To prevent this, we need a **token blacklist system** where refresh tokens can be revoked (blacklisted) on logout.

👉 Use case:

* User logs out → refresh token is blacklisted.
* Any further attempt to use that refresh token → rejected with `"Token is blacklisted"`.

---

## ⚡ Implementation: Logout with Blacklist

### 1. Install extra dependency

```bash
pip install djangorestframework-simplejwt[blacklist]
```

---

### 2. Update `settings.py`

Enable JWT blacklist app:

```python
INSTALLED_APPS = [
    ...
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "users",
    "products",
    "carts",
    "orders",
]
```

---

### 3. Create Logout View (`users/api/v1/views.py`)

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutAPIView(APIView):
    """
    Logout by blacklisting refresh token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
```

---

### 4. Update `users/api/v1/urls.py`

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterAPIView, UserProfileAPIView, LogoutAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", UserProfileAPIView.as_view(), name="user-profile"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
```

---

### 5. Test APIs

#### 1. Logout

* Method: `POST`
* URL: `http://127.0.0.1:8000/api/v1/users/logout/`
* Headers:

```
Authorization: Bearer <access_token>
```

* Body → raw → JSON:

```json
{
  "refresh": "<refresh_token>"
}
```

* Expected Response:

```json
{
  "detail": "Successfully logged out."
}
```

👉 Now if you try to use the **same refresh token** at `/token/refresh/`, you’ll get:

```json
{
  "detail": "Token is blacklisted",
  "code": "token_not_valid"
}
```

---