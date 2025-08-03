# wishlist/utils.py
from .models import Wishlist

def get_user_wishlist(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        wishlist, created = Wishlist.objects.get_or_create(session_key=request.session.session_key)
    return wishlist



def is_in_user_wishlist(request, product):
    user = request.user
    session = request.session

    if user.is_authenticated:
        return product.wishlist_items.filter(wishlist__user=user).exists()

    wishlist = session.get('wishlist', [])
    return product.id in wishlist