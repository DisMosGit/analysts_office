from django.contrib import admin
from django.utils import timezone
from datetime import datetime
from .models import Graph
from server.celery import plot_graph


@admin.register(Graph)
class GraphAdmin(admin.ModelAdmin):
    fields = ("func", "interval", "step")
    list_display = ("func", "points", "interval", "step", "date_processed")
    ordering = ("date_processed", )
    save_as = True

    def reload(self, obj):
        print(obj)
        result = Graph.objects.filter(id=obj).all()
        return result

    def save_model(self, request, obj, form, change):
        obj.save()
        result = plot_graph.apply_async((
            obj.func,
            obj.interval,
            obj.step,
            obj.date_created,
        ),
                                        countdown=3)
        points = result.get()
        obj.points = points
        obj.date_processed = timezone.now()
        obj.save()
