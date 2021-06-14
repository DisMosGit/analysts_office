from django.contrib import admin
from .models import Graph


@admin.register(Graph)
class GraphAdmin(admin.ModelAdmin):
    pass