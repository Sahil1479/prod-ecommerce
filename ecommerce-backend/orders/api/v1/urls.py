from django.urls import path
from .views import OrderListAPIView, OrderDetailAPIView

urlpatterns = [
    path('', OrderListAPIView.as_view(), name='order-list-create-v1'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail-v1'),
]