from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    sync_to_google = forms.BooleanField(required=False, initial=True,
                                        help_text="Also post this job to Google Talent")

    class Meta:
        model = Job
        fields = [
            'title', 'description', 'requirements', 'location',
            'employment_type', 'salary_min', 'salary_max',
            'is_remote', 'apply_url', 'expires_at', 'sync_to_google'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }