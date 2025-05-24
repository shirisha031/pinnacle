from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('master.urls')),  
    path('', include('admission.urls')), # Includes app-level URLs for the routes defined in `master.urls`
    path('', include('attendence.urls')), # Includes app-level URLs for the routes defined in `admission.urls`
]


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)