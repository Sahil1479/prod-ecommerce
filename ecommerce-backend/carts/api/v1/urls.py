from django.urls import path
from .views import CartAPIView, CartItemAPIView

urlpatterns = [
    path('', CartAPIView.as_view(), name='cart-detail'),
    path('items/', CartItemAPIView.as_view(), name='cart-items'),
    path('items/<int:pk>/', CartItemAPIView.as_view(), name='cart-item'),
]