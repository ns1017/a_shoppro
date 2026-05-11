from django import forms

from core.forms import TailwindFormMixin
from customers.models import Vehicle

from .models import Job, JobAttachment
from django.conf import settings


class MultipleFileInput(forms.FileInput):
    """Custom widget that supports multiple file uploads."""
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs['multiple'] = True
        return super().render(name, value, attrs, renderer)


class JobForm(TailwindFormMixin, forms.ModelForm):
    attachments = forms.FileField(
        widget=MultipleFileInput(attrs={'accept': 'image/*,audio/*,.pdf,.doc,.docx'}),
        required=False,
        help_text='Upload images, audio recordings, or documents (Max 25MB per file)'
    )
    attachments_note = forms.CharField(
        required=False,
        max_length=255,
        help_text='Optional note applied to uploaded attachments'
    )
    
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
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        customer_id = self.data.get("customer") or self.initial.get("customer")
        if not customer_id and self.instance.pk:
            customer_id = self.instance.customer_id
        if customer_id:
            self.fields["vehicle"].queryset = Vehicle.objects.filter(customer_id=customer_id).select_related("customer")
        else:
            self.fields["vehicle"].queryset = Vehicle.objects.select_related("customer")
    
    def save(self, commit=True):
        job = super().save(commit=commit)
        
        # Handle file uploads
        note = self.cleaned_data.get('attachments_note') if hasattr(self, 'cleaned_data') else None
        max_size = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', None)
        if self.files.getlist('attachments'):
            for uploaded_file in self.files.getlist('attachments'):
                # Size check (if configured)
                if max_size and uploaded_file.size > max_size:
                    # skip files that exceed limit
                    continue

                # Determine attachment type based on file extension
                ext = uploaded_file.name.split('.')[-1].lower()
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']:
                    att_type = 'image'
                elif ext in ['wav', 'mp3', 'm4a', 'ogg', 'flac']:
                    att_type = 'audio'
                elif ext in ['pdf', 'doc', 'docx', 'txt']:
                    att_type = 'document'
                else:
                    att_type = 'other'

                JobAttachment.objects.create(
                    job=job,
                    file=uploaded_file,
                    attachment_type=att_type,
                    description=note or '',
                    uploaded_by=self.user
                )

        return job
