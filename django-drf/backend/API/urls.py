from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("app/", include("app.urls")),
    path("profile/", include("individual.urls")),
    path("auth/", include("core.urls")),
    # path("__debug__/", include("debug_toolbar.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
