# products/models/product.py

from django.utils.text import slugify
from django.db import models
from decimal import Decimal
from products.models.category import Category


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    description = models.TextField()

    base_price = models.DecimalField(max_digits=10, decimal_places=2)  # Regular price
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Sale price
    in_stock = models.BooleanField(default=True)  # Your requested field

    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.base_price

    def get_final_price(self):
        return self.discount_price if self.has_discount() else self.base_price

    def get_discount_amount(self):
        if self.has_discount():
            return self.base_price - self.discount_price
        return Decimal('0.00')

    def get_discount_percentage(self):
        if self.has_discount() and self.base_price > 0:
            return round((self.get_discount_amount() / self.base_price) * 100)
        return 0

    def get_price_display_data(self):
        return {
            "sale_price": self.discount_price if self.has_discount() else None,
            "regular_price": self.base_price,
            "final_price": self.get_final_price(),
            "savings": self.get_discount_amount(),
            "percentage": self.get_discount_percentage(),
        }
