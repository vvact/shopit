from rest_framework.routers import DefaultRouter
from .views import ProductReviewViewSet

router = DefaultRouter()
router.register(r'reviews', ProductReviewViewSet, basename='review')

urlpatterns = router.urls
