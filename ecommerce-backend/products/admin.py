from django.contrib import admin
from .models import Product, Category, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'created_at', 'seller')
    list_filter = ('category', 'created_at', 'seller')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'user')
    search_fields = ('product__name', 'user__username', 'comment')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

