from rest_framework import serializers
from .models import Order, OrderItem, ShippingAddress
from products.serializers import ProductVariantSerializer
from cart.models import Cart, CartItem

# --- Shipping Address ---
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name', 'phone_number',
            'address_line_1', 'address_line_2',
            'city', 'county', 'postal_code'
        ]

# --- Order Item ---
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'variant', 'quantity', 'price']

# --- Order List / Detail View ---
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'shipping_address',
            'session_key', 'status', 'total',
            'created_at', 'items'
        ]
        read_only_fields = ['user', 'session_key']

# --- Order Creation ---
class OrderCreateSerializer(serializers.Serializer):
    shipping_address = ShippingAddressSerializer()

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        session_key = request.session.session_key if request else None

        cart = Cart.objects.filter(user=user).first() if user else Cart.objects.filter(session_key=session_key).first()
        if not cart or not cart.items.exists():
            raise serializers.ValidationError("Cart is empty")

        # Create order first
        order = Order.objects.create(
            user=user,
            session_key=session_key,
        )

        # Then attach shipping address to order
        shipping_data = validated_data.get('shipping_address')
        ShippingAddress.objects.create(order=order, **shipping_data)

        total = 0
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                quantity=item.quantity,
                price=item.get_price()
            )
            total += item.get_price() * item.quantity

        order.total = total
        order.save()

        # Clear cart
        cart.items.all().delete()

        return order
