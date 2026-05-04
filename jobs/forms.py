from django import forms

from core.forms import TailwindFormMixin
from customers.models import Vehicle

from .models import Job


class JobForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "customer",
            "vehicle",
            "status",
            "service_description",
            "estimated_cost",
            "actual_cost",
            "labor_hours",
            "technician",
            "appointment_date",
        ]
        widgets = {
            "service_description": forms.Textarea(attrs={"rows": 4}),
            "appointment_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customer_id = self.data.get("customer") or self.initial.get("customer")
        if not customer_id and self.instance.pk:
            customer_id = self.instance.customer_id
        if customer_id:
            self.fields["vehicle"].queryset = Vehicle.objects.filter(customer_id=customer_id).select_related("customer")
        else:
            self.fields["vehicle"].queryset = Vehicle.objects.select_related("customer")
