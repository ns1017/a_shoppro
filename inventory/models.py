from django.db import models


class Part(models.Model):
    part_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_demo_data = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.part_number} - {self.name}"
