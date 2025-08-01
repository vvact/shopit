from django.db import models
from products.models.product import Product
from products.models.attribute import Attribute, AttributeValue

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['product', 'attribute', 'value']

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value.value}"