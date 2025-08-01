from django.contrib import admin

# Register your models here.

from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'created_at')
    search_fields = ('user__username', 'session_key')
    readonly_fields = ('created_at',)
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'variant', 'quantity', 'added_at')
    search_fields = ('cart__session_key', 'product__name', 'variant__name')
    readonly_fields = ('added_at',)
    list_filter = ('cart__user', 'added_at')

