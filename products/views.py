# products/views.py

from rest_framework import viewsets, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
# products/views.py
from rest_framework import viewsets
from django.utils import timezone
from .models import FlashDeal
from .serializers import FlashDealSerializer

from .models import Product, Category
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategorySerializer
)
from .filters import ProductFilter


# ---- Category Views ----
class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        slug = self.request.query_params.get('slug')

        if slug:
            return Category.objects.filter(slug=slug)

        return (
            Category.objects
            .filter(parent__isnull=True)
            .annotate(
                direct_products=Count('products', distinct=True),
                child_products=Count('children__products', distinct=True)
            )
            .filter(Q(direct_products__gt=0) | Q(child_products__gt=0))
            .prefetch_related('children')
            .order_by('name')
        )


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


# ---- Product Views ----

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related(
        'images', 'variants', 'attributes__attribute', 'attributes__value'
    ).select_related('category')
    lookup_field = 'slug'

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

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




class FlashDealViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FlashDealSerializer

    def get_queryset(self):
        now = timezone.now()
        return FlashDeal.objects.filter(
            is_active=True,
            start_time__lte=now,
            end_time__gte=now
        )
