from django.contrib import admin
from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import activate

activate('ru')

urlpatterns = [
    re_path(
        r'^favicon\.ico$',
        RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico',
                             permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + i18n_patterns(
        path('admin/', admin.site.urls))
