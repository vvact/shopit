from rest_framework import serializers
from .models import (
    Category,
    Product,
    ProductImage,
    ProductVariant,
    Attribute,
    AttributeValue,
    ProductAttribute,
    Color,
    Size,
)

# ---- CATEGORY SERIALIZER ----
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


# ---- IMAGE SERIALIZER ----
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_main', 'position']


# ---- COLOR / SIZE SERIALIZERS ----
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']


# ---- ATTRIBUTE / VALUE SERIALIZERS ----
class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'value']


class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = ['id', 'name', 'values']


# ---- PRODUCT ATTRIBUTE SERIALIZER ----
class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute = serializers.StringRelatedField()
    value = serializers.StringRelatedField()

    class Meta:
        model = ProductAttribute
        fields = ['attribute', 'value']


# ---- PRODUCT VARIANT SERIALIZER ----
class ProductVariantSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'color', 'size', 'image',
            'is_active', 'created_at', 'updated_at'
        ]


# ---- PRODUCT LIST SERIALIZER (lightweight) ----
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


# ---- PRODUCT DETAIL SERIALIZER ----
class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    discount_amount = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'description',
            'base_price', 'discount_price', 'price',
            'discount_amount', 'discount_percentage',
            'in_stock', 'is_available', 'is_featured',
            'created_at', 'updated_at',
            'images', 'variants', 'attributes'
        ]

    def get_discount_amount(self, obj):
        return obj.get_discount_amount()

    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()

    def get_price(self, obj):
        return obj.get_final_price()
