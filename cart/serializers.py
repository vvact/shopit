from rest_framework import serializers
from .models import Cart, CartItem
from products.models import ProductVariant, Product
from products.serializers import ProductListSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(),
        source='variant',
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'product_id',
            'variant',
            'variant_id',
            'quantity',
        ]
        read_only_fields = ['id', 'product', 'variant']

    def create(self, validated_data):
        cart = self.context['cart']
        product = validated_data['product']
        variant = validated_data.get('variant')
        quantity = validated_data.get('quantity', 1)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        return item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'session_key',
            'created_at',
            'items',
        ]
        read_only_fields = ['id', 'user', 'session_key', 'created_at', 'items']
