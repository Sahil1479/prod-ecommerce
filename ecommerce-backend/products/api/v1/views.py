import logging
from django.shortcuts import get_object_or_404
from httpx import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Product, Category, ProductSubscription, Review
from .serializers import ProductSerializer, CategorySerializer, ProductSubscriptionSerializer, ReviewSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Permission imports
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.api.v1.permissions import IsCustomer, IsAdmin, IsSeller

# Caching imports
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# Throttling imports
from products.throttles import ProductSubscriptionThrottle

# Logging imports
from ecommerce.logging_helper import log_event

# Pagination imports
from rest_framework.pagination import PageNumberPagination

# Custom Pagination Class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryListAPIView(APIView):
    """
    List all categories.
    """
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST","PUT", "DELETE"]:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]  # default fallback

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetailAPIView(APIView):
    """
    Retrieve, update or delete a category instance.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]  # default fallback

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ReviewListCreateAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]  # default fallback

    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, product_id):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product_id=product_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReviewDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAuthenticated(), (IsCustomer() | IsAdmin())]
        return [IsAuthenticated()]  # default fallback

    def put(self, request, pk):
        review = get_object_or_404(Review, pk=pk, user=request.user)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = get_object_or_404(Review, pk=pk, user=request.user)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProductListAPIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAuthenticated(), (IsAdmin() | IsSeller())]
        return [IsAuthenticated()]  # default fallback

    """
        This decorator caches the entire response for the view.
        By default, it caches per full URL (path + query params). No need to manually cache. using cache.get() or cache.set().
        Any user hitting /products/ will get the cached response.
    """
    @method_decorator(cache_page(60*2))  # Cache for 2 minutes
    def get(self, request):
        log_event("fetch_products_start", payload={"path": request.path}, level="INFO")

        try:
            products = Product.objects.all().order_by('-created_at')
            paginator = StandardResultsSetPagination()
            result_page = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(result_page, many=True)
            log_event(
                "fetch_products_success",
                payload={"count": products.count()},
                level="INFO"
            )
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            log_event("fetch_products_error", payload={"error": str(e)}, level="ERROR")
            return Response({"detail": "Error fetching products"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        if not request.user.is_staff and request.user.role != 'seller':
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetailAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAuthenticated(), (IsAdmin() | IsSeller())]
        return [IsAuthenticated()]  # default fallback

    """
        Here we are manually caching the product detail view.
        We first check if the product is in cache using cache.get().
        If not, we fetch from DB and store it in cache using cache.set().
    """
    def get(self, request, pk):
        log_event("fetch_product_details_start", payload={"product_id": pk}, level="INFO")
        cache_key = f'product_{pk}'
        product = cache.get(cache_key)
        if not product:
            product = get_object_or_404(Product, pk=pk)
            cache.set(cache_key, product, timeout=60*5)  # Cache for 5 minutes
            log_event("fetch_product_details_cache_set", payload={"product_id": pk}, level="INFO")
        else:
            log_event("fetch_product_details_cache_hit", payload={"product_id": pk}, level="INFO")
        serializer = ProductSerializer(product)
        log_event("fetch_product_details_success", payload={"product_id": pk}, level="INFO")
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.is_staff and product.seller != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f'product_{pk}')  # Delete from cache as the product is updated (Cache Invalidation)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.is_staff and product.seller != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        cache.delete(f'product_{pk}')  # Delete from cache as the product is deleted (Cache Invalidation)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProductSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]
    throttle_classes = [UserRateThrottle, AnonRateThrottle, ProductSubscriptionThrottle]

    def post(self, request):
        serializer = ProductSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUnsubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def delete(self, request, pk):
        subscription = get_object_or_404(ProductSubscription, pk=pk, user=request.user)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)