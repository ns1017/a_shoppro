from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from .forms import CustomerForm, VehicleForm
from .models import Customer, Vehicle

from core.utils import log_activity


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = "customers/customer_list.html"
    context_object_name = "customers"

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("vehicles")
        search = self.request.GET.get("q")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(phone__icontains=search)
                | Q(email__icontains=search)
            )
        return queryset


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "customers/customer_detail.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("vehicles", "jobs__vehicle")


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customer_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            log_activity(self.request.user, "created", "Customer", self.object.id, extra=self.object.name)
        except Exception:
            pass
        return response


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customer_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            log_activity(self.request.user, "updated", "Customer", self.object.id, extra=self.object.name)
        except Exception:
            pass
        return response


class CustomerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Customer
    template_name = "customers/customer_confirm_delete.html"
    success_url = reverse_lazy("customer_list")

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        customer_name = obj.name
        response = super().delete(request, *args, **kwargs)
        try:
            log_activity(self.request.user, "deleted", "Customer", obj.id, extra=customer_name)
        except Exception:
            pass
        return response


class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = "customers/vehicle_list.html"
    context_object_name = "vehicles"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("customer")
        search = self.request.GET.get("q")
        if search:
            queryset = queryset.filter(
                Q(vin__icontains=search)
                | Q(make__icontains=search)
                | Q(model__icontains=search)
                | Q(license_plate__icontains=search)
                | Q(customer__name__icontains=search)
            )
        return queryset


class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "customers/vehicle_form.html"
    success_url = reverse_lazy("vehicle_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            log_activity(self.request.user, "created", "Vehicle", self.object.id, extra=f"{self.object.vin} {self.object.make} {self.object.model}")
        except Exception:
            pass
        return response


class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = "customers/vehicle_form.html"
    success_url = reverse_lazy("vehicle_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            log_activity(self.request.user, "updated", "Vehicle", self.object.id, extra=f"{self.object.vin} {self.object.make} {self.object.model}")
        except Exception:
            pass
        return response


class VehicleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vehicle
    template_name = "customers/vehicle_confirm_delete.html"
    success_url = reverse_lazy("vehicle_list")

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        vehicle_label = f"{obj.vin} {obj.make} {obj.model}"
        response = super().delete(request, *args, **kwargs)
        try:
            log_activity(self.request.user, "deleted", "Vehicle", obj.id, extra=vehicle_label)
        except Exception:
            pass
        return response
