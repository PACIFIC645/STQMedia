from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# Define URL patterns
urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    path('theme/', include('theme.urls')),

    # Include stqpictures URLs with namespace
    path('', include('stqpictures.urls', namespace='stqpictures')),
]

# Add static and media file handling for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
