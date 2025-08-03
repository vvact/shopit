# wishlist/urls.py

from django.urls import path
from .views import ToggleWishlistView, WishlistView

urlpatterns = [
    path('', WishlistView.as_view(), name='wishlist'),
    path('toggle/<int:product_id>/', ToggleWishlistView.as_view(), name='toggle-wishlist'),
]
