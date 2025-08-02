from rest_framework import serializers
from django.db.models import Avg

from reviews.serializers import ReviewSerializer
from .models import (
    Category, Product, ProductImage, ProductVariant,
    Attribute, AttributeValue, ProductAttribute,
    Color, Size
)
from products import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_main', 'position']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'value']


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'values']


class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = serializers.StringRelatedField()
    value = serializers.StringRelatedField()

    class Meta:
        model = ProductAttribute
        fields = ['attribute', 'value']


class ProductVariantSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'color', 'size', 'image',
            'is_active', 'created_at', 'updated_at'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    main_image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category',
            'price', 'main_image', 'is_featured',
        ]

    def get_main_image(self, obj):
        image = obj.images.filter(is_main=True).first()
        return image.image.url if image else None

    def get_price(self, obj):
        return obj.get_final_price()


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    attributes = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    has_variants = serializers.BooleanField(read_only=True)

    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True, source='product_reviews')  # 👈 Optional

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'description',
            'base_price', 'discount_price', 'price',
            'discount_amount', 'discount_percentage',
            'in_stock', 'is_available', 'is_featured',
            'created_at', 'updated_at',
            'images', 'has_variants', 'variants', 'attributes',
            'average_rating', 'review_count', 'reviews',  # 👈 reviews optional
        ]

    def get_average_rating(self, obj):
        return obj.product_reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    def get_review_count(self, obj):
        return obj.product_reviews.count()

    def get_discount_amount(self, obj):
        return obj.get_discount_amount()

    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()

    def get_price(self, obj):
        return obj.get_final_price()

    def get_attributes(self, obj):
        return {
            attr.attribute.name: attr.value.value
            for attr in obj.attributes.all()
        }