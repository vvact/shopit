# products/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer
from .filters import ProductFilter  # <- Import your custom filter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related(
        'images', 'variants', 'attributes__attribute', 'attributes__value'
    ).select_related('category')
    lookup_field = 'slug'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer

    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        product = self.get_object()
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]
        serializer = ProductListSerializer(
            related_products, many=True, context={'request': request}
        )
        return Response(serializer.data)
