from django.contrib import admin

from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "object_type", "object_id")
    search_fields = ("user__username", "action", "object_type", "object_id", "extra")
    readonly_fields = ("timestamp", "user", "action", "object_type", "object_id", "extra")
    ordering = ("-timestamp",)
