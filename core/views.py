from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

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


@login_required
def calendar_events(request):
    """Return JSON list of Jobs with appointment_date for FullCalendar.

    Accepts `start` and `end` GET params (ISO datetimes) and filters
    appointment_date between them when provided.
    """
    start = request.GET.get("start")
    end = request.GET.get("end")

    events_qs = Job.objects.exclude(appointment_date__isnull=True)
    try:
        if start:
            start_dt = parse_datetime(start)
            if start_dt:
                events_qs = events_qs.filter(appointment_date__gte=start_dt)
        if end:
            end_dt = parse_datetime(end)
            if end_dt:
                events_qs = events_qs.filter(appointment_date__lte=end_dt)
    except Exception:
        # on parse failure, fall back to returning all with appointment_date
        pass

    events = []
    for job in events_qs:
        if not job.appointment_date:
            continue
        title = f"{job.vehicle} - {job.technician or 'Unassigned'}"
        events.append({
            "id": job.pk,
            "title": title,
            "start": timezone.localtime(job.appointment_date).strftime("%Y-%m-%dT%H:%M:%S"),
            "url": f"/jobs/{job.pk}/",
        })

    return JsonResponse(events, safe=False)
