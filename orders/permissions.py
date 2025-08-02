from rest_framework.permissions import BasePermission, SAFE_METHODS

class AllowPostAnyUser(BasePermission):
    """
    Allow anyone to POST, but restrict other methods.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated
