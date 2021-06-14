from datetime import datetime
from io import BytesIO

from django.contrib import admin
from django.utils import timezone

from django.core.files.images import ImageFile

from server.celery import plot_graph_by_data
from .models import Graph


@admin.register(Graph)
class GraphAdmin(admin.ModelAdmin):
    fields = ("func", "interval", "step")
    list_display = ("func", "image", "interval", "step", "date_processed")
    ordering = ("date_processed", )
    actions = ('refresh', )
    save_as = True

    @admin.action(description='Refresh graphs')
    def refresh(self, request, queryset):
        print(queryset, request)
        queryset.update(date_processed=datetime.now())

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

    @admin.action(description='Refresh graphs')
    def refresh(self, request, queryset):
        for obj in queryset:
            self.update_plot(obj)

    def save_model(self, request, obj: Graph, form, change):
        obj.save()
        self.update_plot(obj)
