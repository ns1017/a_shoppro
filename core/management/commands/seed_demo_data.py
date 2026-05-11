from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from customers.models import Customer, Vehicle
from inventory.models import Part
from jobs.models import Job, JobPart


class Command(BaseCommand):
    help = "Seed a comprehensive set of demo records for local development."

    def add_arguments(self, parser):
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Delete all demo data before seeding new data',
        )

    def handle(self, *args, **options):
        if options['cleanup']:
            self.cleanup_demo_data()

        # Create demo admin user
        User = get_user_model()
        admin_user, created = User.objects.get_or_create(
            username="manager",
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "email": "manager@example.com",
                "first_name": "Demo",
                "last_name": "Manager",
            },
        )
        if created:
            self.stdout.write(f"✓ Created admin user: {admin_user.username}")

        # Create demo parts (20+)
        self.stdout.write("\n📦 Creating demo parts...")
        parts_data = [
            ("OIL-01", "Synthetic Oil 5W-30", "Full synthetic motor oil, 5 quarts", 12, 4, 45.99),
            ("OIL-02", "Conventional Oil 10W-40", "Conventional motor oil, 5 quarts", 8, 3, 28.99),
            ("FLTR-01", "Engine Air Filter", "High-efficiency cabin air filter", 15, 5, 22.50),
            ("FLTR-02", "Cabin Air Filter", "Standard cabin air filter", 20, 6, 18.75),
            ("FLTR-03", "Oil Filter Short", "Standard spin-on oil filter", 25, 8, 8.50),
            ("FLTR-04", "Oil Filter Long", "Extended-length oil filter", 10, 4, 12.99),
            ("BRAK-01", "Brake Pad Set Front", "Semi-metallic front brake pads", 5, 2, 65.00),
            ("BRAK-02", "Brake Pad Set Rear", "Organic rear brake pads", 7, 3, 55.00),
            ("BRAK-03", "Brake Fluid DOT 3", "Premium brake fluid, 1 quart", 12, 4, 12.99),
            ("BELT-01", "Serpentine Belt", "Multi-groove serpentine belt", 4, 2, 35.50),
            ("BELT-02", "Timing Belt", "Reinforced timing belt", 2, 1, 89.99),
            ("COOL-01", "Coolant 50/50 Mix", "Pre-mixed coolant, 1 gallon", 15, 5, 18.50),
            ("COOL-02", "Coolant Concentrate", "Concentrated coolant, 1 gallon", 8, 3, 22.99),
            ("COOL-03", "Thermostat Housing", "Complete thermostat assembly", 3, 1, 45.00),
            ("SPARK-01", "Spark Plugs (4-pack)", "OEM spark plugs, set of 4", 10, 4, 24.99),
            ("SPARK-02", "Spark Plugs (8-pack)", "OEM spark plugs, set of 8", 6, 2, 42.99),
            ("WIPR-01", "Wiper Blade Set", "All-season wiper blades, pair", 20, 6, 32.00),
            ("BATT-01", "Car Battery 12V 75Ah", "Standard lead-acid battery", 4, 2, 129.99),
            ("FLUD-01", "Transmission Fluid", "ATF synthetic blend, 1 quart", 10, 4, 14.50),
            ("FLUD-02", "Power Steering Fluid", "Synthetic PSF, 1 quart", 8, 3, 16.99),
            ("PAD-01", "Brake Caliper Pads", "Ceramic brake pads", 6, 2, 72.50),
            ("HOSE-01", "Radiator Hose Upper", "Reinforced upper radiator hose", 5, 2, 28.00),
            ("HOSE-02", "Radiator Hose Lower", "Reinforced lower radiator hose", 4, 1, 32.50),
        ]
        parts = {}
        for part_number, name, description, qty, reorder, cost in parts_data:
            part, created = Part.objects.get_or_create(
                part_number=part_number,
                defaults={
                    "name": name,
                    "description": description,
                    "quantity_in_stock": qty,
                    "reorder_level": reorder,
                    "unit_cost": cost,
                    "is_demo_data": True,
                },
            )
            parts[part_number] = part
            if created:
                self.stdout.write(f"  ✓ {part_number}: {name}")

        # Create demo customers (3-5)
        self.stdout.write("\n👥 Creating demo customers...")
        customers_data = [
            {
                "name": "Jordan Taylor",
                "phone": "555-0142",
                "email": "jordan@example.com",
                "address": "100 Main Street, Springfield, IL 62701",
                "notes": "Prefers text updates. Has two vehicles.",
            },
            {
                "name": "Sam Chen",
                "phone": "555-0156",
                "email": "sam.chen@example.com",
                "address": "425 Oakwood Avenue, Chicago, IL 60601",
                "notes": "Business owner, fleet maintenance.",
            },
            {
                "name": "Maria Rodriguez",
                "phone": "555-0189",
                "email": "mrodriguez@example.com",
                "address": "750 Pine Road, Aurora, IL 60505",
                "notes": "Loyal customer since 2019. Prefers email communication.",
            },
            {
                "name": "James Wilson",
                "phone": "555-0203",
                "email": "jwilson@example.com",
                "address": "321 Elm Street, Naperville, IL 60540",
                "notes": "New customer. Referred by Maria.",
            },
            {
                "name": "Patricia Lee",
                "phone": "555-0217",
                "email": "plee@example.com",
                "address": "892 Maple Drive, Evanston, IL 60201",
                "notes": "Regular maintenance schedule preferred.",
            },
        ]
        customers = {}
        for cust_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                name=cust_data["name"],
                defaults={
                    "phone": cust_data["phone"],
                    "email": cust_data["email"],
                    "address": cust_data["address"],
                    "notes": cust_data["notes"],
                    "is_demo_data": True,
                },
            )
            customers[cust_data["name"]] = customer
            if created:
                self.stdout.write(f"  ✓ {cust_data['name']}")

        # Create demo vehicles (5-10)
        self.stdout.write("\n🚗 Creating demo vehicles...")
        vehicles_data = [
            ("1HGCM82633A123456", "Jordan Taylor", 2020, "Honda", "Civic", "AUTO-101", 28450),
            ("2T1BF1K31FC135742", "Jordan Taylor", 2019, "Toyota", "Corolla", "AUTO-102", 35200),
            ("5TDJKRFH4LS123456", "Sam Chen", 2022, "Toyota", "Sienna", "AUTO-103", 12800),
            ("1G1FB1S58F0103467", "Sam Chen", 2021, "Chevrolet", "Cruze", "AUTO-104", 18500),
            ("5FNYF6H72LB123456", "Maria Rodriguez", 2023, "Honda", "Odyssey", "AUTO-105", 6200),
            ("3VWGE21C07M000001", "James Wilson", 2018, "Volkswagen", "Jetta", "AUTO-106", 52100),
            ("1FTFW1ET5DFC10247", "Patricia Lee", 2021, "Ford", "F-150", "AUTO-107", 22300),
            ("JH2RC5004M0200321", "Maria Rodriguez", 2017, "Honda", "CB Motorcycle", "MOTO-001", 8900),
        ]
        vehicles = {}
        for vin, customer_name, year, make, model, plate, mileage in vehicles_data:
            vehicle, created = Vehicle.objects.get_or_create(
                vin=vin,
                defaults={
                    "customer": customers[customer_name],
                    "year": year,
                    "make": make,
                    "model": model,
                    "license_plate": plate,
                    "mileage": mileage,
                    "is_demo_data": True,
                    "notes": f"{year} {make} {model} in good condition",
                },
            )
            vehicles[vin] = vehicle
            if created:
                self.stdout.write(f"  ✓ {year} {make} {model} ({plate})")

        # Create demo jobs (10-15)
        self.stdout.write("\n🔧 Creating demo jobs...")
        job_statuses = [Job.Status.COMPLETED, Job.Status.READY, Job.Status.IN_BAY, Job.Status.WAITING]
        job_data = [
            {
                "vehicle_vin": "1HGCM82633A123456",
                "service": "Oil change and filter replacement",
                "estimated_cost": 75.00,
                "actual_cost": 78.50,
                "labor_hours": 0.5,
                "technician": "Alex",
                "status": Job.Status.COMPLETED,
                "parts": ["OIL-01", "FLTR-03"],
                "days_ago": 3,
            },
            {
                "vehicle_vin": "1HGCM82633A123456",
                "service": "Brake pad replacement and inspection",
                "estimated_cost": 180.00,
                "actual_cost": 195.00,
                "labor_hours": 1.5,
                "technician": "Jordan",
                "status": Job.Status.COMPLETED,
                "parts": ["BRAK-01", "BRAK-03"],
                "days_ago": 12,
            },
            {
                "vehicle_vin": "2T1BF1K31FC135742",
                "service": "Routine maintenance: fluids and filters",
                "estimated_cost": 120.00,
                "actual_cost": 0,
                "labor_hours": 1.0,
                "technician": "Casey",
                "status": Job.Status.READY,
                "parts": ["OIL-02", "FLTR-01", "FLTR-02"],
                "days_ago": 0,
            },
            {
                "vehicle_vin": "5TDJKRFH4LS123456",
                "service": "Coolant flush and refill",
                "estimated_cost": 95.00,
                "actual_cost": 0,
                "labor_hours": 0.75,
                "technician": "Alex",
                "status": Job.Status.IN_BAY,
                "parts": ["COOL-01", "COOL-02"],
                "days_ago": 0,
            },
            {
                "vehicle_vin": "1G1FB1S58F0103467",
                "service": "Air filter and cabin filter replacement",
                "estimated_cost": 65.00,
                "actual_cost": 68.00,
                "labor_hours": 0.5,
                "technician": "Jordan",
                "status": Job.Status.COMPLETED,
                "parts": ["FLTR-01", "FLTR-02"],
                "days_ago": 5,
            },
            {
                "vehicle_vin": "5FNYF6H72LB123456",
                "service": "Spark plug replacement",
                "estimated_cost": 85.00,
                "actual_cost": 0,
                "labor_hours": 1.0,
                "technician": "Casey",
                "status": Job.Status.WAITING,
                "parts": ["SPARK-01"],
                "days_ago": 1,
            },
            {
                "vehicle_vin": "3VWGE21C07M000001",
                "service": "Belt inspection and serpentine belt replacement",
                "estimated_cost": 125.00,
                "actual_cost": 132.50,
                "labor_hours": 1.25,
                "technician": "Alex",
                "status": Job.Status.COMPLETED,
                "parts": ["BELT-01"],
                "days_ago": 8,
            },
            {
                "vehicle_vin": "1FTFW1ET5DFC10247",
                "service": "Full brake system service",
                "estimated_cost": 250.00,
                "actual_cost": 265.00,
                "labor_hours": 2.0,
                "technician": "Jordan",
                "status": Job.Status.COMPLETED,
                "parts": ["BRAK-01", "BRAK-02", "BRAK-03"],
                "days_ago": 2,
            },
            {
                "vehicle_vin": "JH2RC5004M0200321",
                "service": "Tire rotation and balance",
                "estimated_cost": 55.00,
                "actual_cost": 0,
                "labor_hours": 0.75,
                "technician": "Casey",
                "status": Job.Status.WAITING,
                "parts": [],
                "days_ago": 0,
            },
            {
                "vehicle_vin": "1HGCM82633A123456",
                "service": "Battery replacement",
                "estimated_cost": 165.00,
                "actual_cost": 0,
                "labor_hours": 0.5,
                "technician": "Alex",
                "status": Job.Status.IN_BAY,
                "parts": ["BATT-01"],
                "days_ago": 0,
            },
            {
                "vehicle_vin": "2T1BF1K31FC135742",
                "service": "Transmission fluid service",
                "estimated_cost": 120.00,
                "actual_cost": 128.00,
                "labor_hours": 1.0,
                "technician": "Jordan",
                "status": Job.Status.COMPLETED,
                "parts": ["FLUD-01"],
                "days_ago": 15,
            },
            {
                "vehicle_vin": "5TDJKRFH4LS123456",
                "service": "Wiper blade replacement and inspection",
                "estimated_cost": 45.00,
                "actual_cost": 0,
                "labor_hours": 0.25,
                "technician": "Casey",
                "status": Job.Status.READY,
                "parts": ["WIPR-01"],
                "days_ago": 0,
            },
            {
                "vehicle_vin": "1G1FB1S58F0103467",
                "service": "Power steering fluid check and top off",
                "estimated_cost": 35.00,
                "actual_cost": 0,
                "labor_hours": 0.25,
                "technician": "Alex",
                "status": Job.Status.WAITING,
                "parts": ["FLUD-02"],
                "days_ago": 0,
            },
            {
                "vehicle_vin": "5FNYF6H72LB123456",
                "service": "General vehicle inspection",
                "estimated_cost": 50.00,
                "actual_cost": 50.00,
                "labor_hours": 0.75,
                "technician": "Jordan",
                "status": Job.Status.COMPLETED,
                "parts": [],
                "days_ago": 20,
            },
            {
                "vehicle_vin": "3VWGE21C07M000001",
                "service": "Radiator hose replacement and coolant top off",
                "estimated_cost": 110.00,
                "actual_cost": 0,
                "labor_hours": 1.0,
                "technician": "Alex",
                "status": Job.Status.IN_BAY,
                "parts": ["HOSE-01", "COOL-01"],
                "days_ago": 0,
            },
        ]

        jobs_created = 0
        for job_info in job_data:
            vehicle = vehicles[job_info["vehicle_vin"]]
            customer = vehicle.customer

            # Calculate appointment date based on days_ago
            days_ago = job_info["days_ago"]
            base_time = timezone.now()
            appointment_time = base_time - timedelta(days=days_ago)
            # Ensure WAITING (scheduled) jobs fall within the next 36 hours
            # so they appear on the Kanban "Scheduled (Next 36 Hours)" column.
            if job_info["status"] == Job.Status.WAITING:
                appointment_time = base_time + timedelta(hours=24)

            job, created = Job.objects.get_or_create(
                customer=customer,
                vehicle=vehicle,
                service_description=job_info["service"],
                defaults={
                    "status": job_info["status"],
                    "estimated_cost": job_info["estimated_cost"],
                    "actual_cost": job_info["actual_cost"],
                    "labor_hours": job_info["labor_hours"],
                    "technician": job_info["technician"],
                    "appointment_date": appointment_time,
                    "is_demo_data": True,
                },
            )

            if created:
                jobs_created += 1
                # Add parts to job
                for part_number in job_info["parts"]:
                    part = parts[part_number]
                    JobPart.objects.get_or_create(
                        job=job,
                        part=part,
                        defaults={
                            "quantity_used": 1,
                            "is_demo_data": True,
                        },
                    )

        self.stdout.write(f"  ✓ Created {jobs_created} jobs with associated parts")

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("✅ Demo data seeded successfully!"))
        self.stdout.write("=" * 50)
        self.stdout.write(f"\n📊 Summary:")
        self.stdout.write(f"  • Customers: {len(customers)}")
        self.stdout.write(f"  • Vehicles: {len(vehicles)}")
        self.stdout.write(f"  • Parts: {len(parts)}")
        self.stdout.write(f"  • Jobs: {jobs_created}")
        self.stdout.write(
            f"\n💡 Tip: Run 'python manage.py delete_demo_data' to remove all demo records.\n"
        )

    def cleanup_demo_data(self):
        """Delete all existing demo data before seeding."""
        self.stdout.write("🧹 Cleaning up existing demo data...")

        count = 0
        for model_class in [Job, JobPart, Vehicle, Customer, Part]:
            deleted_count, _ = model_class.objects.filter(is_demo_data=True).delete()
            count += deleted_count
            if deleted_count > 0:
                self.stdout.write(f"  ✓ Deleted {deleted_count} {model_class.__name__} records")

        if count == 0:
            self.stdout.write("  No demo data to clean up")
        else:
            self.stdout.write(f"  Total: {count} records deleted\n")

