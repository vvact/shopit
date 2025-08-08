from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryDetailView, FlashDealViewSet, ProductViewSet, CategoryListView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('', include(router.urls)),
    # Add any additional product-related URLs here
    path('flash-deals/', FlashDealViewSet.as_view({'get': 'list'}), name='flash-deal-list'),
]
