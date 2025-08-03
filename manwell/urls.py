from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    # include your app's URLs here
    path('api/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/', include('orders.urls')),
    path('api/', include ('users.urls')),
    path('api/', include('reviews.urls')),
    path('api/wishlist/', include('wishlist.urls')),
    path('api/payments/', include('payments.urls')),



]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
