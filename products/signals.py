# products/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from .models import Category

def update_category_product_count(category):
    if category:
        category.product_count = category.products.count()
        category.save()

@receiver(post_save, sender=Product)
def product_saved(sender, instance, **kwargs):
    update_category_product_count(instance.category)

@receiver(post_delete, sender=Product)
def product_deleted(sender, instance, **kwargs):
    update_category_product_count(instance.category)
