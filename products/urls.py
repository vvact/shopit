from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CategoryDetailView, ProductViewSet, CategoryListView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('', include(router.urls)),
]
