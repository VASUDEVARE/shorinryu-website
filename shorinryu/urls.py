from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header  = "Shorin Ryu Karate Do India — Admin"
admin.site.site_title   = "SRKDI Admin"
admin.site.index_title  = "Website Management Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)