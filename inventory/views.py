from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import PartForm
from .models import Part


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
