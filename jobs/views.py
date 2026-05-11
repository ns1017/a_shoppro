from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from datetime import timedelta

from .forms import JobForm
from .models import Job, JobAttachment
from django.db import models

from core.utils import log_activity


class JobBoardView(LoginRequiredMixin, TemplateView):
    template_name = "jobs/job_board.html"

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        upcoming_cutoff = now + timedelta(hours=36)
        completed_cutoff = now - timedelta(hours=36)

        context.update(
            {
                "scheduled_jobs": Job.objects.filter(
                    status=Job.Status.WAITING,
                    appointment_date__isnull=False,
                    appointment_date__gte=now,
                    appointment_date__lte=upcoming_cutoff,
                )
                .select_related("customer", "vehicle")
                .order_by("appointment_date", "created_at"),
                "in_bay_jobs": Job.objects.filter(status=Job.Status.IN_BAY)
                .select_related("customer", "vehicle")
                .order_by("appointment_date", "created_at"),
                "completed_jobs": Job.objects.filter(
                    status=Job.Status.COMPLETED,
                    updated_at__gte=completed_cutoff,
                )
                .select_related("customer", "vehicle")
                .order_by("-updated_at"),
            }
        )
        return context


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("job_board")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            log_activity(self.request.user, "created", "Job", self.object.id, extra=form.cleaned_data.get("service_description", ""))
        except Exception:
            pass
        return response


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("job_board")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            log_activity(self.request.user, "updated", "Job", self.object.id, extra=form.cleaned_data.get("service_description", ""))
        except Exception:
            pass
        return response


class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = "jobs/job_detail.html"


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = "jobs/job_confirm_delete.html"
    success_url = reverse_lazy("job_board")

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        oid = obj.id
        response = super().delete(request, *args, **kwargs)
        try:
            log_activity(self.request.user, "deleted", "Job", oid, extra=str(obj.service_description)[:200])
        except Exception:
            pass
        return response


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "jobs/job_list.html"
    context_object_name = "jobs"
    paginate_by = 20

    def get_queryset(self):
        qs = (
            Job.objects.select_related("customer", "vehicle").all().order_by("-created_at")
        )
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                models.Q(service_description__icontains=q)
                | models.Q(technician__icontains=q)
                | models.Q(customer__name__icontains=q)
                | models.Q(vehicle__vin__icontains=q)
                | models.Q(vehicle__make__icontains=q)
                | models.Q(vehicle__model__icontains=q)
            )
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs


@require_POST
@login_required
def update_job_status(request, pk):
    job = get_object_or_404(Job, pk=pk)
    status = request.POST.get("status")
    valid_statuses = {choice for choice, _label in Job.Status.choices}
    if status not in valid_statuses:
        return JsonResponse({"ok": False, "error": "Invalid status."}, status=400)

    now = timezone.now()
    if status == Job.Status.WAITING:
        if not job.appointment_date:
            return JsonResponse(
                {
                    "ok": False,
                    "error": "Scheduled jobs must have an appointment date.",
                },
                status=400,
            )
        if not (now <= job.appointment_date <= now + timedelta(hours=36)):
            return JsonResponse(
                {
                    "ok": False,
                    "error": "Scheduled jobs must be within the next 36 hours. Update the appointment time first.",
                },
                status=400,
            )

    if status == Job.Status.COMPLETED and job.appointment_date and job.appointment_date > now + timedelta(days=3):
        return JsonResponse(
            {
                "ok": False,
                "error": "Jobs scheduled more than 3 days out cannot be marked completed. Update the appointment time first.",
            },
            status=400,
        )

    old = job.status
    job.status = status
    job.save(update_fields=["status", "updated_at"])
    try:
        log_activity(request.user, "status_changed", "Job", job.id, extra=f"{old} -> {status}")
    except Exception:
        pass
    return JsonResponse({"ok": True, "status": job.status})


@login_required
def get_vehicles_by_customer(request):
    """Return vehicles for a given customer as JSON."""
    from customers.models import Vehicle
    
    customer_id = request.GET.get("customer_id")
    if not customer_id:
        return JsonResponse({"vehicles": []})
    
    try:
        vehicles = Vehicle.objects.filter(customer_id=int(customer_id)).values("id", "year", "make", "model", "license_plate", "vin")
        return JsonResponse({"vehicles": list(vehicles)})
    except (ValueError, TypeError):
        return JsonResponse({"vehicles": []}, status=400)


@require_POST
@login_required
def delete_job_attachment(request, pk, attachment_id):
    """Delete a job attachment. Only staff or the uploader can delete."""
    job = get_object_or_404(Job, pk=pk)
    attachment = get_object_or_404(JobAttachment, pk=attachment_id, job=job)
    
    # Permission check - allow if staff or uploader
    if not (request.user.is_staff or request.user == attachment.uploaded_by):
        raise Http404()
    
    attachment.file.delete()
    attachment.delete()
    
    return redirect('job_detail', pk=pk)
