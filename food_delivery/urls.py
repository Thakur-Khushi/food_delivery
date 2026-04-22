"""
Main URL Configuration for Food Delivery App
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),        # Home + Menu pages
    path('', include('users.urls')),       # Login, Register, Logout
    path('cart/', include('cart.urls')),   # Cart pages
    path('orders/', include('orders.urls')), # Orders pages
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
