from django.contrib import admin

from .models import Job, JobPart


class JobPartInline(admin.TabularInline):
    model = JobPart
    extra = 0


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "customer", "status", "technician", "appointment_date", "created_at")
    list_filter = ("status", "appointment_date", "created_at")
    search_fields = ("customer__name", "vehicle__vin", "vehicle__make", "vehicle__model", "technician")
    autocomplete_fields = ("customer", "vehicle")
    inlines = [JobPartInline]
