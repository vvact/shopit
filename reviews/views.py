from rest_framework import viewsets, permissions
from .models import ProductReview
from .serializers import ReviewSerializer
from .permissions import IsReviewOwnerOrReadOnly


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
