from django.contrib import admin

from .models import Customer, Vehicle


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "created_at")
    search_fields = ("name", "phone", "email")
    list_filter = ("created_at",)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("year", "make", "model", "customer", "vin", "license_plate", "mileage")
    search_fields = ("vin", "license_plate", "make", "model", "customer__name")
    list_filter = ("make", "year")
    autocomplete_fields = ("customer",)
