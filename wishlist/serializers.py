# wishlist/serializers.py
from rest_framework import serializers
from .models import WishlistItem
from products.serializers import ProductListSerializer

class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'product', 'added_at']
