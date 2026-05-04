from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("customers", "0001_initial"),
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobPart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity_used", models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("waiting", "Waiting"), ("in_bay", "In Bay"), ("ready", "Ready for Pickup"), ("completed", "Completed")], default="waiting", max_length=20)),
                ("service_description", models.TextField()),
                ("estimated_cost", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("actual_cost", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("labor_hours", models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ("technician", models.CharField(blank=True, max_length=120)),
                ("appointment_date", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("customer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="jobs", to="customers.customer")),
                ("vehicle", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="jobs", to="customers.vehicle")),
                ("parts", models.ManyToManyField(blank=True, related_name="jobs", through="JobPart", to="inventory.part")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddField(
            model_name="jobpart",
            name="job",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="job_parts", to="jobs.job"),
        ),
        migrations.AddField(
            model_name="jobpart",
            name="part",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="job_parts", to="inventory.part"),
        ),
        migrations.AlterUniqueTogether(
            name="jobpart",
            unique_together={("job", "part")},
        ),
    ]

