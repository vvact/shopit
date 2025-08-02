from rest_framework import generics, permissions
from .models import ProductReview
from .serializers import ReviewSerializer
from orders.models import OrderItem
from rest_framework import serializers

class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        user = self.request.user

        has_purchased = OrderItem.objects.filter(
            order__user=user,
            product=product,
            order__status='delivered'
        ).exists()

        if not has_purchased:
            raise serializers.ValidationError("You can only review products you've purchased and received.")

        serializer.save(user=user)
