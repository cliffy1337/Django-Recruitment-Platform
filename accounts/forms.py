from django import forms
from allauth.account.forms import SignupForm
from .models import User

class CustomSignupForm(SignupForm):
    """
    Custom signup form that extends allauth's SignupForm
    """
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label='I am a'
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        label='Phone Number'
    )
    company_name = forms.CharField(
        max_length=255,
        required=False,
        label='Company Name (if recruiter)'
    )
    
    def save(self, request):
        user = super().save(request)
        
        # Set additional fields
        user.user_type = self.cleaned_data['user_type']
        user.phone = self.cleaned_data.get('phone', '')
        
        # Only set company name for recruiters
        if user.user_type == 'recruiter':
            user.company_name = self.cleaned_data.get('company_name', '')
        
        user.save()
        return user