# products/filters.py
import django_filters
from products.models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    # Filter by category id
    category_id = django_filters.NumberFilter(field_name="category__id", lookup_expr="exact")

    # OR filter by category name (case-insensitive)
    category_name = django_filters.CharFilter(field_name="category__name", lookup_expr="iexact")

    class Meta:
        model = Product
        fields = ["min_price", "max_price", "category_id", "category_name"]
