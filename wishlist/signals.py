# wishlist/signals.py
from django.contrib.auth.signals import user_logged_in
from .models import Wishlist, WishlistItem

def merge_wishlist_on_login(sender, user, request, **kwargs):
    session_key = request.session.session_key
    if session_key:
        try:
            session_wishlist = Wishlist.objects.get(session_key=session_key, user__isnull=True)
            user_wishlist, _ = Wishlist.objects.get_or_create(user=user)
            for item in session_wishlist.items.all():
                WishlistItem.objects.get_or_create(wishlist=user_wishlist, product=item.product)
            session_wishlist.delete()
        except Wishlist.DoesNotExist:
            pass

user_logged_in.connect(merge_wishlist_on_login)
