vafrom django.db import models

from customers.models import Customer, Vehicle


class Job(models.Model):
    class Status(models.TextChoices):
        WAITING = "waiting", "Scheduled"
        IN_BAY = "in_bay", "In Bay"
        READY = "ready", "Ready"
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


class JobAttachment(models.Model):
    ATTACHMENT_TYPES = [
        ('image', 'Image'),
        ('audio', 'Audio Recording'),
        ('document', 'Document'),
        ('other', 'Other'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='job_attachments/%Y/%m/%d/')
    attachment_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPES, default='other')
    description = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self) -> str:
        return f"{self.job} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
