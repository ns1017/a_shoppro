from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from jobs.models import Job


class ReportView(LoginRequiredMixin, View):
    template_name = "reports/report_dashboard.html"

    def get(self, request):
        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())

        daily_jobs = Job.objects.filter(created_at__date=today)
        weekly_jobs = Job.objects.filter(created_at__date__gte=week_start)

        context = {
            "daily_job_count": daily_jobs.count(),
            "weekly_job_count": weekly_jobs.count(),
            "daily_revenue": daily_jobs.aggregate(total=Sum("actual_cost")).get("total") or 0,
            "weekly_revenue": weekly_jobs.aggregate(total=Sum("actual_cost")).get("total") or 0,
            "status_breakdown": Job.objects.values("status").annotate(total=Count("id")).order_by("status"),
            "recent_completed_jobs": Job.objects.filter(status=Job.Status.COMPLETED).select_related("customer", "vehicle")[:10],
        }
        return render(request, self.template_name, context)
