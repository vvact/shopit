from rest_framework import permissions
from orders.models import OrderItem

class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to all users.
    Only the review owner can update or delete.
    """

    def has_object_permission(self, request, view, obj):
        # Safe methods are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        # Otherwise only the owner can modify
        return obj.user == request.user


class HasPurchasedProduct(permissions.BasePermission):
    """
    Only allow users to review products they have purchased and had delivered.
    """

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True  # Only restrict creation

        product_id = request.data.get('product')
        if not product_id:
            return False

        return OrderItem.objects.filter(
            order__user=request.user,
            product_id=product_id,
            order__status='delivered'
        ).exists()
