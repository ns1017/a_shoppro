from django.db import models

from customers.models import Customer, Vehicle


class Job(models.Model):
    class Status(models.TextChoices):
        WAITING = "waiting", "Waiting"
        IN_BAY = "in_bay", "In Bay"
        READY = "ready", "Ready for Pickup"
        COMPLETED = "completed", "Completed"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="jobs")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="jobs")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.WAITING)
    service_description = models.TextField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    labor_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    technician = models.CharField(max_length=120, blank=True)
    appointment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parts = models.ManyToManyField("inventory.Part", through="JobPart", related_name="jobs", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.vehicle} - {self.customer}"


class JobPart(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_parts")
    part = models.ForeignKey("inventory.Part", on_delete=models.CASCADE, related_name="job_parts")
    quantity_used = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("job", "part")

    def __str__(self) -> str:
        return f"{self.job} - {self.part}"
