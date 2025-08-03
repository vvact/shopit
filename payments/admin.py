from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'payment_method', 'status', 'transaction_id', 'created_at']
    search_fields = ['transaction_id', 'phone_number']

