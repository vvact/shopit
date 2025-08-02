from django.contrib import admin

from .models import ProductReview
# Register your models here.



@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__email')
    list_filter = ('rating', 'created_at')

