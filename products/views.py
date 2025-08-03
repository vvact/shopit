# products/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from .models import Product
from .serializers import ProductListSerializer, ProductDetailSerializer
from .filters import ProductFilter  # <- Import your custom filter


from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True).order_by('name')
    serializer_class = CategorySerializer

    def get_queryset(self):
        slug = self.request.query_params.get('slug')
        if slug:
            return Category.objects.filter(slug=slug)
        return Category.objects.filter(parent__isnull=True).prefetch_related('children').order_by('name')
    

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class TopLevelCategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True).order_by('name')
    serializer_class = CategorySerializer




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
