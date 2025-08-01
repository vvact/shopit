from django.db import models
from products.models.product import Product

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)

    is_main = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)  # Optional: controls display order
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position', '-created_at']  # show in order, newest last if same position

    def __str__(self):
        return f"Image for {self.product.name}"
