from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def my_applications(request):
    return render(request, 'applications/my_applications.html')