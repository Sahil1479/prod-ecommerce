Here are summarized instructions for adding JWT authentication to your Django project (based on your backend structure):

### Steps to Add JWT Auth in Django

1. **Install Dependencies**

   - Install `djangorestframework` and a JWT package (e.g., `djangorestframework-simplejwt`):
     ```
     pip install djangorestframework djangorestframework-simplejwt
     ```

2. **Update `settings.py`**

   - Add `'rest_framework'` and `'rest_framework_simplejwt'` to `INSTALLED_APPS`.
   - Configure REST framework to use JWT authentication:
     ```python
     REST_FRAMEWORK = {
         'DEFAULT_AUTHENTICATION_CLASSES': (
             'rest_framework_simplejwt.authentication.JWTAuthentication',
         ),
     }
     ```
   - Optionally, configure JWT settings (token lifetime, etc.):
     ```python
     from datetime import timedelta
     SIMPLE_JWT = {
         'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
         'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
         # ...other options
     }
     ```

3. **Add JWT Endpoints to `urls.py`**

   - In your main or users app `urls.py`:

     ```python
     from rest_framework_simplejwt.views import (
         TokenObtainPairView,
         TokenRefreshView,
     )

     urlpatterns = [
         # ...other urls
         path('api/v1/users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
         path('api/v1/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     ]
     ```

4. **Protect API Views**

   - Use DRF permissions to require authentication:

     ```python
     from rest_framework.permissions import IsAuthenticated

     class MyProtectedView(APIView):
         permission_classes = [IsAuthenticated]
         # ...view code
     ```

5. **Frontend Integration**
   - Use the `/api/v1/users/token/` endpoint to obtain access and refresh tokens.
   - Use `/api/v1/users/token/refresh/` to refresh tokens when expired.
   - Send the access token in the `Authorization: Bearer <token>` header for protected requests.

---

**Notes for Reference:**

- JWT tokens are stateless and do not require server-side sessions.
- Always use HTTPS in production to protect tokens.
- Store refresh tokens securely; do not expose them to client-side JS if possible.
- You can customize user claims and token payloads via `TokenObtainPairSerializer`.

Let me know if you want a more detailed step-by-step guide or code samples for any part!5. **Frontend Integration**

- Use the `/api/v1/users/token/` endpoint to obtain access and refresh tokens.
- Use `/api/v1/users/token/refresh/` to refresh tokens when expired.
- Send the access token in the `Authorization: Bearer <token>` header for protected requests.

---

**Notes for Reference:**

- JWT tokens are stateless and do not require server-side sessions.
- Always use HTTPS in production to protect tokens.
- Store refresh tokens securely; do not expose them to client-side JS if possible.
- You can customize user claims and token payloads via `TokenObtainPairSerializer`.

Let me know if you want a more detailed step-by-step guide or code samples for any part!
