from datetime import datetime

from django.contrib import admin
from django.utils import timezone, html
from django.conf import settings
from django.utils.translation import gettext as _

from server.celery import plot_graph_by_data
from .models import Graph


@admin.register(Graph)
class GraphAdmin(admin.ModelAdmin):
    fields = ("func", "interval", "step")
    list_display = ("func", "tumblar", "interval", "step", "date_processed")
    ordering = ("date_processed", )
    actions = ('refresh', )
    save_as = True

    @admin.display(description=_("graph"))
    def tumblar(self, obj):
        if obj.error:
            return html.mark_safe(f'<span>{obj.error}</span>')
        return html.mark_safe(
            f'<img src="{settings.MEDIA_URL + html.escape(obj.image)}" width="200" height="200" alt="{html.escape(obj.image)}"/>'
        )

    def update_plot(self, obj: Graph):
        result = plot_graph_by_data.apply_async(
            (
                obj.func,
                obj.interval,
                obj.step,
                obj.date_created,
            ),
            countdown=3,
        )
        try:
            path = result.get()
            obj.image = path
        except Exception as e:
            obj.error = str(e)
        obj.date_processed = timezone.now()
        obj.save()

    @admin.action(description=_("Refresh"))
    def refresh(self, request, queryset):
        for obj in queryset:
            self.update_plot(obj)

    def save_model(self, request, obj: Graph, form, change):
        obj.save()
        self.update_plot(obj)
