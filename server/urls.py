from django.contrib import admin
from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(
        r'^favicon\.ico$',
        RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico',
                             permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
