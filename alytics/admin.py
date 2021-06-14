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
    save_as = True

    def reload(self, obj):
        print(obj)
        result = Graph.objects.filter(id=obj).all()
        return result

    def save_model(self, request, obj: Graph, form, change):
        obj.save()
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
