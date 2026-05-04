from django import forms

from core.forms import TailwindFormMixin

from .models import Part


class PartForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Part
        fields = [
            "part_number",
            "name",
            "description",
            "quantity_in_stock",
            "reorder_level",
            "unit_cost",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
