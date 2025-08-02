from rest_framework import serializers
from .models import ProductReview
from .utils import user_has_purchased

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'product', 'rating', 'review', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        product = data.get('product')

        # Check if user purchased and received the product
        if not user_has_purchased(user, product):
            raise serializers.ValidationError("You can only review products you've received.")

        # Check if user already reviewed this product
        if ProductReview.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product.")

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
