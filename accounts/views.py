from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')