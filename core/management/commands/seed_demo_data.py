from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from customers.models import Customer, Vehicle
from inventory.models import Part
from jobs.models import Job


class Command(BaseCommand):
    help = "Seed a small set of demo records for local development."

    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.get_or_create(
            username="manager",
            defaults={"is_staff": True, "is_superuser": True, "email": "manager@example.com"},
        )

        customer, _ = Customer.objects.get_or_create(
            name="Jordan Taylor",
            defaults={
                "phone": "555-0142",
                "email": "jordan@example.com",
                "address": "100 Main Street",
                "notes": "Prefers text updates.",
            },
        )

        vehicle, _ = Vehicle.objects.get_or_create(
            vin="1HGCM82633A123456",
            defaults={
                "customer": customer,
                "year": 2020,
                "make": "Honda",
                "model": "Civic",
                "license_plate": "AUTO-101",
                "mileage": 28450,
                "notes": "Oil change every 5k miles.",
            },
        )

        part, _ = Part.objects.get_or_create(
            part_number="FLTR-010",
            defaults={
                "name": "Oil Filter",
                "description": "Standard spin-on oil filter.",
                "quantity_in_stock": 12,
                "reorder_level": 4,
                "unit_cost": 8.50,
            },
        )

        job, _ = Job.objects.get_or_create(
            customer=customer,
            vehicle=vehicle,
            service_description="Customer reports routine service and inspection.",
            defaults={
                "status": Job.Status.WAITING,
                "estimated_cost": 149.99,
                "actual_cost": 0,
                "labor_hours": 1.5,
                "technician": "Alex",
            },
        )
        job.parts.add(part)

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
