# wishlist/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from products.models import Product
from .models import Wishlist, WishlistItem
from .serializers import WishlistItemSerializer
from .utils import get_user_wishlist


class WishlistView(APIView):
    def get(self, request):
        wishlist = get_user_wishlist(request)
        items = wishlist.items.all()
        serializer = WishlistItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        wishlist = get_user_wishlist(request)
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
            return Response({'detail': 'Product added to wishlist.'}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        wishlist = get_user_wishlist(request)
        product_id = request.data.get('product_id')
        try:
            item = wishlist.items.get(product_id=product_id)
            item.delete()
            return Response({'detail': 'Product removed from wishlist.'})
        except WishlistItem.DoesNotExist:
            return Response({'error': 'Item not found in wishlist.'}, status=status.HTTP_404_NOT_FOUND)


class ToggleWishlistView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, product_id):
        user = request.user
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_authenticated:
            wishlist, _ = Wishlist.objects.get_or_create(user=user)
            item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
            if not created:
                item.delete()
                return Response({'status': 'removed'}, status=status.HTTP_200_OK)
            return Response({'status': 'added'}, status=status.HTTP_201_CREATED)
        else:
            session = request.session
            wishlist = session.get('wishlist', [])
            if product_id in wishlist:
                wishlist.remove(product_id)
                session['wishlist'] = wishlist
                return Response({'status': 'removed'})
            else:
                wishlist.append(product_id)
                session['wishlist'] = wishlist
                return Response({'status': 'added'})
