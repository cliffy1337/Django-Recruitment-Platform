from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import User
from .forms import CustomSignupForm
from allauth.account.views import SignupView

class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'account/signup.html'

@login_required
def dashboard(request):
    """
    User dashboard based on user type
    """
    if request.user.is_recruiter:
        return render(request, 'accounts/recruiter_dashboard.html')
    else:
        return render(request, 'accounts/job_seeker_dashboard.html')

@login_required
def profile(request):
    """
    Edit user profile
    """
    if request.method == 'POST':
        # Handle profile update
        user = request.user
        
        # Update fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        
        if user.is_recruiter:
            user.company_name = request.POST.get('company_name', user.company_name)
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        # Handle resume upload
        if 'resume' in request.FILES and user.is_job_seeker:
            user.resume = request.FILES['resume']
        
        user.save()
        messages.success(request, _('Profile updated successfully'))
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html', {'user': request.user})