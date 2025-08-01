from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404

class CartViewSet(viewsets.ViewSet):
    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
            session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

    def list(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart = self.get_cart(request)
        data = request.data.copy()
        data['cart'] = cart.id

        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            variant = serializer.validated_data.get('variant', None)
            quantity = serializer.validated_data['quantity']

            item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                variant=variant,
                defaults={'quantity': quantity}
            )
            if not created:
                item.quantity += quantity
                item.save()

            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def update_item(self, request):
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        variant_id = request.data.get('variant_id')
        quantity = request.data.get('quantity')

        if not product_id or quantity is None:
            return Response({'error': 'product_id and quantity required'}, status=400)

        try:
            item = CartItem.objects.get(
                cart=cart,
                product_id=product_id,
                variant_id=variant_id
            )
            item.quantity = quantity
            item.save()
            return Response(CartSerializer(cart).data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=404)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        cart = self.get_cart(request)
        product_id = request.data.get('product_id')
        variant_id = request.data.get('variant_id')

        try:
            item = CartItem.objects.get(
                cart=cart,
                product_id=product_id,
                variant_id=variant_id
            )
            item.delete()
            return Response(CartSerializer(cart).data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)

    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = self.get_cart(request)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)
