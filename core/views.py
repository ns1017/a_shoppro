from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from customers.models import Customer, Vehicle
from jobs.models import Job


@login_required
def dashboard(request):
    today = timezone.localdate()
    month_start = today.replace(day=1)

    jobs_today = Job.objects.filter(created_at__date=today).count()
    jobs_scheduled = Job.objects.filter(appointment_date__date__gte=today).count()
    waiting_parts = Job.objects.filter(status=Job.Status.WAITING).count()
    total_revenue_mtd = (
        Job.objects.filter(status=Job.Status.COMPLETED, created_at__date__gte=month_start)
        .aggregate(total=Sum("actual_cost"))
        .get("total")
        or 0
    )
    recent_jobs = Job.objects.select_related("customer", "vehicle").order_by("-created_at")[:8]

    context = {
        "jobs_today": jobs_today,
        "jobs_scheduled": jobs_scheduled,
        "waiting_parts": waiting_parts,
        "total_revenue_mtd": total_revenue_mtd,
        "recent_jobs": recent_jobs,
        "customer_count": Customer.objects.count(),
        "vehicle_count": Vehicle.objects.count(),
    }
    return render(request, "core/dashboard.html", context)
