from django.apps import AppConfig


class WishlistConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wishlist"
    verbose_name = "Wishlist Management"
    label = "wishlist"
    def ready(self):
        # Import signals or any other startup code here if needed
        import wishlist.signals
