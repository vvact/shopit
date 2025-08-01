# products/models/variant.py

from django.db import models
from products.models.product import Product
from products.models.color import Color
from products.models.size import Size


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='variants/', blank=True, null=True)

    is_active = models.BooleanField(default=True)  # NEW: optional control over visibility
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # NEW
    # is_default = models.BooleanField(default=False)  # Optional: mark default combo

    class Meta:
        unique_together = ('product', 'color', 'size')

    def __str__(self):
        return self.get_variant_name()

    def get_variant_name(self):
        return f"{self.product.name} - {self.color.name} - {self.size.name}"
