from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'created_at', 'total_price']
    list_filter = ['created_at']
    search_fields = ['user__email', 'session_key']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    list_filter = ['order']
    search_fields = ['product__name']


from .models import Order, OrderItem, ShippingAddress



admin.site.register(ShippingAddress)

