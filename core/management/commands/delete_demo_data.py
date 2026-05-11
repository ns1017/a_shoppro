from django.core.management.base import BaseCommand

from core.models import ActivityLog
from customers.models import Customer, Vehicle
from inventory.models import Part
from jobs.models import Job, JobPart, JobAttachment


class Command(BaseCommand):
    help = "Delete all demo data marked with is_demo_data=True. This cannot be undone!"

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-confirm',
            action='store_true',
            help='Delete without asking for confirmation (useful for scripts/CI)',
        )

    def handle(self, *args, **options):
        """Delete all demo data from the database."""
        
        # Count demo records across all models
        demo_counts = {
            "Job": Job.objects.filter(is_demo_data=True).count(),
            "JobPart": JobPart.objects.filter(is_demo_data=True).count(),
            "JobAttachment": JobAttachment.objects.filter(is_demo_data=True).count(),
            "Vehicle": Vehicle.objects.filter(is_demo_data=True).count(),
            "Customer": Customer.objects.filter(is_demo_data=True).count(),
            "Part": Part.objects.filter(is_demo_data=True).count(),
            "ActivityLog": ActivityLog.objects.filter(is_demo_data=True).count(),
        }

        total_records = sum(demo_counts.values())

        if total_records == 0:
            self.stdout.write(self.style.SUCCESS("✅ No demo data found to delete."))
            return

        # Display summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.WARNING("⚠️  DEMO DATA DELETION REPORT"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"\n📊 Demo records that will be deleted:\n")

        for model_name, count in demo_counts.items():
            if count > 0:
                self.stdout.write(f"  • {model_name}: {count} record{'s' if count != 1 else ''}")

        self.stdout.write(f"\n  {'─' * 56}")
        self.stdout.write(f"  📈 Total: {total_records} record{'s' if total_records != 1 else ''}")
        self.stdout.write("=" * 60)

        # Ask for confirmation unless --no-confirm flag is used
        if not options['no_confirm']:
            self.stdout.write("\n" + self.style.ERROR("❌ WARNING: This action cannot be undone!"))
            confirm = input("\n🤔 Are you sure you want to delete all demo data? (type 'yes' to confirm): ")

            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING("\n✋ Deletion cancelled. No data was deleted.\n"))
                return

        # Perform deletion in dependency order
        # Delete in this order: JobAttachment → JobPart → Job → Vehicle → Customer → Part → ActivityLog
        self.stdout.write("\n🗑️  Deleting demo data...\n")

        deletion_order = [
            ("JobAttachment", JobAttachment),
            ("JobPart", JobPart),
            ("Job", Job),
            ("Vehicle", Vehicle),
            ("Customer", Customer),
            ("Part", Part),
            ("ActivityLog", ActivityLog),
        ]

        total_deleted = 0
        for model_name, model_class in deletion_order:
            deleted_count, _ = model_class.objects.filter(is_demo_data=True).delete()
            if deleted_count > 0:
                self.stdout.write(
                    f"  ✓ Deleted {deleted_count} {model_name} record{'s' if deleted_count != 1 else ''}"
                )
                total_deleted += deleted_count

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(
            self.style.SUCCESS(f"✅ Successfully deleted {total_deleted} demo record{'s' if total_deleted != 1 else ''}!")
        )
        self.stdout.write("=" * 60 + "\n")
