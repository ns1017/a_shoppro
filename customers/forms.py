from django import forms

from core.forms import TailwindFormMixin

from .models import Customer, Vehicle


class CustomerForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "phone", "email", "address", "notes"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class VehicleForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["customer", "vin", "year", "make", "model", "license_plate", "mileage", "notes"]
        widgets = {
            "vin": forms.TextInput(attrs={"autocomplete": "off"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_vin(self):
        return self.cleaned_data["vin"].strip().upper()
