from django.urls import path
from .views import LogoutAPIView, UserDetailAPIView, UserListAPIView, RegisterAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("profile/<int:pk>/", UserDetailAPIView.as_view(), name="user-profile-v1"),
    path("list/", UserListAPIView.as_view(), name="user-list-v1"),
    path("register/", RegisterAPIView.as_view(), name="user-register-v1"),
    
    # Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair-v1'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh-v1'),
    path("logout/", LogoutAPIView.as_view(), name="logout-v1"),
]