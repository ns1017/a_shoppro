from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_demo_data = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="vehicles")
    vin = models.CharField(max_length=17, unique=True)
    year = models.PositiveIntegerField()
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=50, blank=True)
    mileage = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_demo_data = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.vin = (self.vin or "").strip().upper()
        self.license_plate = (self.license_plate or "").strip().upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.year} {self.make} {self.model}"
