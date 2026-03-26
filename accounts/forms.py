from django import forms
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from .models import User, Education, WorkExperience, Skill


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
    
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        company_name = cleaned_data.get('company_name')
        
        if user_type == 'recruiter' and not company_name:
            self.add_error('company_name', 'Company name is required for recruiters.')
        
        return cleaned_data
    
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


class ProfileForm(forms.ModelForm):
    """
    Form for editing profile information
    """
    class Meta:
        model = User
        fields = ['username', 'phone', 'company_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 8900'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.is_recruiter:
            self.fields['company_name'].required = True
            self.fields['company_name'].label = 'Company Name *'
        else:
            self.fields['company_name'].widget = forms.HiddenInput()
            self.fields['company_name'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        if self.instance and self.instance.is_recruiter:
            company_name = cleaned_data.get('company_name')
            if not company_name:
                self.add_error('company_name', 'Company name is required for recruiters.')
        return cleaned_data


class ProfilePictureForm(forms.ModelForm):
    """
    Form for profile picture upload
    """
    class Meta:
        model = User
        fields = ['profile_picture']
    
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Validate file size (max 5MB)
            if picture.size > 5 * 1024 * 1024:
                raise ValidationError('Profile picture must be less than 5MB')
            
            # Validate file type
            valid_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if picture.content_type not in valid_types:
                raise ValidationError('Please upload a valid image file (JPEG, PNG, GIF, or WebP)')
            
            # Validate file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            import os
            ext = os.path.splitext(picture.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError('Invalid file extension. Allowed: jpg, jpeg, png, gif, webp')
        
        return picture


class EducationForm(forms.ModelForm):
    """Form for adding/editing education"""
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'current', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        current = cleaned_data.get('current')
        
        if not current and end_date and start_date and end_date < start_date:
            raise ValidationError('End date cannot be before start date')
        
        return cleaned_data


class WorkExperienceForm(forms.ModelForm):
    """Form for adding/editing work experience"""
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company', 'location', 'start_date', 'end_date', 'current', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        current = cleaned_data.get('current')
        
        if not current and end_date and start_date and end_date < start_date:
            raise ValidationError('End date cannot be before start date')
        
        return cleaned_data


class SkillForm(forms.ModelForm):
    """Form for adding/editing skills"""
    class Meta:
        model = Skill
        fields = ['name', 'years_of_experience']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Python, Django, Project Management'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }