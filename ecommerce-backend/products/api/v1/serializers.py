from rest_framework import serializers
from products.models import Product, Category, ProductSubscription, Review
from users.api.v1.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    seller = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'created_at', 'seller']


class ProductSubscriptionSerializer(serializers.Serializer):
    class Meta:
        model = ProductSubscription
        fields = ['id', 'user', 'product', 'subscribed_at']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "product", "rating", "comment", "created_at"]
