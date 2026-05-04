from django.contrib import admin

from .models import Part


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("part_number", "name", "quantity_in_stock", "reorder_level", "unit_cost")
    search_fields = ("part_number", "name")
    list_filter = ("created_at",)
