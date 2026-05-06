from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .forms import PartForm
from .models import Part
from core.utils import log_activity


class PartListView(LoginRequiredMixin, ListView):
    model = Part
    template_name = "inventory/part_list.html"
    context_object_name = "parts"


class PartCreateView(LoginRequiredMixin, CreateView):
    model = Part
    form_class = PartForm
    template_name = "inventory/part_form.html"
    success_url = reverse_lazy("part_list")


class PartUpdateView(LoginRequiredMixin, UpdateView):
    model = Part
    form_class = PartForm
    template_name = "inventory/part_form.html"
    success_url = reverse_lazy("part_list")


class PartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Part
    template_name = "inventory/part_confirm_delete.html"
    success_url = reverse_lazy("part_list")

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        part_label = f"{obj.part_number} {obj.name}"
        response = super().delete(request, *args, **kwargs)
        try:
            log_activity(self.request.user, "deleted", "Part", obj.id, extra=part_label)
        except Exception:
            pass
        return response
