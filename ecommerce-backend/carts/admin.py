from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', )
    list_filter = ('user',)
    search_fields = ('user__username', 'user__email',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    list_filter = ('cart', 'product')
    search_fields = ('cart__user__username', 'cart__user__email', 'product__name')
    ordering = ('-id',)
