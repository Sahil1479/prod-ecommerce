from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView, CategoryListAPIView, CategoryDetailAPIView, ProductSubscriptionAPIView, ProductUnsubscribeAPIView, ReviewListCreateAPIView, ReviewDetailAPIView, ProductSubscriptionAPIView, ProductUnsubscribeAPIView

urlpatterns = [
    path("", ProductListAPIView.as_view(), name="product-list-v1"),
    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail-v1"),
    path("categories/", CategoryListAPIView.as_view(), name="category-list-v1"),
    path("categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="category-detail-v1"),
    path("<int:product_id>/reviews/", ReviewListCreateAPIView.as_view(), name="review-list-create-v1"),
    path("<int:product_id>/subscribe/", ProductSubscriptionAPIView.as_view(), name="product-subscribe"),
    path("<int:product_id>/unsubscribe/", ProductUnsubscribeAPIView.as_view(), name="product-unsubscribe"),
    path("reviews/<int:pk>/", ReviewDetailAPIView.as_view(), name="review-detail-v1"),
]