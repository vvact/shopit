from rest_framework import serializers
from django.db.models import Avg

from reviews.serializers import ReviewSerializer
from .models import (
    Category, Product, ProductImage, ProductVariant,
    Attribute, AttributeValue, ProductAttribute,
    Color, Size
)
from wishlist.utils import is_in_user_wishlist
from django.db.models import Count

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    breadcrumbs = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'children', 'level', 'product_count', 'breadcrumbs']

    def get_children(self, obj):
         # ✅ Only return children with product_count > 0
        children = obj.children.annotate(
            actual_product_count=Count("products")
        ).filter(actual_product_count__gt=0)
        return [
            {
                'id': child.id,
                'name': child.name,
                'slug': child.slug,
                'product_count': child.actual_product_count,
            }
            for child in children
        ]

    def get_product_count(self, obj):
        def collect_descendants(cat):
            
            descendants = list(cat.children.all())
            for child in cat.children.all():
                descendants.extend(collect_descendants(child))
            return descendants

        categories = [obj] + collect_descendants(obj)
        return Product.objects.filter(category__in=categories).count()

    def get_level(self, obj):
        level = 0
        parent = obj.parent
        while parent:
            level += 1
            parent = parent.parent
        return level

    def get_breadcrumbs(self, obj):
        slugs = []
        names = []
        current = obj
        while current:
            slugs.insert(0, current.slug)
            names.insert(0, current.name)
            current = current.parent
        return {
            "path": '/' + '/'.join(slugs),
            "label": ' > '.join(names)
        }



# products/serializers.py

class CategoryNestedSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    parent_name = serializers.SerializerMethodField()
    breadcrumbs = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent_name', 'level', 'breadcrumbs']

    def get_level(self, obj):
        level = 0
        current = obj.parent
        while current:
            level += 1
            current = current.parent
        return level

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None

    def get_breadcrumbs(self, obj):
        slugs = []
        names = []
        current = obj
        while current:
            slugs.insert(0, current.slug)
            names.insert(0, current.name)
            current = current.parent
        return {
            "path": '/' + '/'.join(slugs),
            "label": ' > '.join(names)
        }


# --- Images ---
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_main', 'position']


# --- Color & Size ---
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']


# --- Attribute & Values ---
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


# --- Variant ---
class ProductVariantSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'color', 'size', 'image',
            'is_active', 'created_at', 'updated_at'
        ]


# --- Product List ---
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


class ProductCategorySerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'level',]



    def get_level(self, obj):
        level = 0
        parent = obj.parent
        while parent:
            level += 1
            parent = parent.parent
        return level



# --- Product Detail ---
class ProductDetailSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    attributes = serializers.SerializerMethodField()
    discount_amount = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    has_variants = serializers.BooleanField(read_only=True)

    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True, source='product_reviews')
    is_in_wishlist = serializers.SerializerMethodField()
    variant_attributes = serializers.SerializerMethodField()
    breadcrumbs = serializers.SerializerMethodField()
    related_products = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'description',
            'base_price', 'discount_price', 'price',
            'discount_amount', 'discount_percentage',
            'in_stock', 'is_available', 'is_featured',
            'created_at', 'updated_at',
            'images', 'has_variants', 'variants', 'attributes',
            'average_rating', 'review_count', 'reviews',
            'is_in_wishlist', 'variant_attributes', 'breadcrumbs',
            'related_products',
        ]

    def get_related_products(self, obj):
        related_qs = Product.objects.filter(
            category=obj.category, is_available=True
        ).exclude(id=obj.id)[:4]  # Limit to 4, exclude current
        return ProductListSerializer(related_qs, many=True).data

    def get_variant_attributes(self, obj):
        color_names = sorted(
            obj.variants.values_list('color__name', flat=True).distinct()
        )
        size_names = sorted(
            obj.variants.values_list('size__name', flat=True).distinct()
        )
        return {
            "Color": list(color_names),
            "Size": list(size_names)
        }

    def get_is_in_wishlist(self, obj):
        request = self.context.get('request')
        return is_in_user_wishlist(request, obj)

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
    

    def get_breadcrumbs(self, obj):
        slugs = []
        names = []
        current = obj.category  # Ensure this points to the category object
        while current:
            slugs.insert(0, current.slug)
            names.insert(0, current.name)
            current = current.parent
        return {
            "path": '/' + '/'.join(slugs),
            "label": ' > '.join(names)
        }