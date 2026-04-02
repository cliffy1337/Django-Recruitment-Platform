from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import json

from .models import User, Education, WorkExperience, Skill
from .forms import ProfileForm, ProfilePictureForm, EducationForm, WorkExperienceForm, SkillForm


@login_required
def dashboard(request):
    """User dashboard view"""
    # You can add counts from other apps here
    context = {
        'user': request.user,
        'is_recruiter': request.user.is_recruiter,
        'is_job_seeker': request.user.is_job_seeker,
        'onboarding_completed': request.user.onboarding_completed,
        # Add these counts from your applications and jobs apps
        'total_applications': 0,  # Replace with actual count
        'total_jobs_posted': 0,    # Replace with actual count
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    """Profile view with edit functionality"""
    user = request.user
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('accounts:profile')
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = ProfileForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
        'profile_picture_form': ProfilePictureForm(instance=user),
        'is_recruiter': user.is_recruiter,
        'is_job_seeker': user.is_job_seeker,
        'onboarding_completed': user.onboarding_completed,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def upload_profile_picture(request):
    """Handle profile picture upload via AJAX"""
    try:
        user = request.user
        form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            # Save the new picture
            form.save()
            
            return JsonResponse({
                'success': True,
                'url': user.profile_picture.url,
                'message': 'Profile picture updated successfully'
            })
        else:
            # Collect all errors
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = [str(error) for error in field_errors]
            
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_profile_picture(request):
    """Delete profile picture"""
    try:
        user = request.user
        
        if not user.profile_picture:
            return JsonResponse({
                'success': False,
                'error': 'No profile picture to delete'
            }, status=400)
        
        # Delete the picture using the model method
        user.delete_profile_picture()
        
        return JsonResponse({
            'success': True,
            'message': 'Profile picture deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def upload_resume(request):
    """Handle resume upload"""
    try:
        user = request.user
        if 'resume' in request.FILES:
            file = request.FILES['resume']
            
            if file.size > 5 * 1024 * 1024:
                return JsonResponse({'success': False, 'error': 'File size must be less than 5MB'}, status=400)
            
            if user.resume:
                user.resume.delete(save=False)
            
            user.resume = file
            user.save()
            
            return JsonResponse({'success': True, 'message': 'Resume uploaded successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'No file provided'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_resume(request):
    """Delete resume"""
    try:
        user = request.user
        if user.resume:
            user.resume.delete(save=False)
            user.resume = None
            user.save()
            return JsonResponse({'success': True, 'message': 'Resume deleted successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'No resume to delete'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# Education Views
@login_required
def add_education(request):
    """Add education entry"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = EducationForm(data)
            if form.is_valid():
                education = form.save(commit=False)
                education.user = request.user
                education.save()
                return JsonResponse({'success': True, 'message': 'Education added successfully'})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def edit_education(request, pk):
    """Edit education entry"""
    education = get_object_or_404(Education, pk=pk, user=request.user)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': education.id,
            'institution': education.institution,
            'degree': education.degree,
            'field_of_study': education.field_of_study,
            'start_date': education.start_date.isoformat(),
            'end_date': education.end_date.isoformat() if education.end_date else None,
            'current': education.current,
            'description': education.description
        })
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = EducationForm(data, instance=education)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Education updated successfully'})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def delete_education(request, pk):
    """Delete education entry"""
    education = get_object_or_404(Education, pk=pk, user=request.user)
    if request.method == 'DELETE':
        education.delete()
        return JsonResponse({'success': True, 'message': 'Education deleted successfully'})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


# Work Experience Views
@login_required
def add_work_experience(request):
    """Add work experience entry"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = WorkExperienceForm(data)
            if form.is_valid():
                work = form.save(commit=False)
                work.user = request.user
                work.save()
                return JsonResponse({'success': True, 'message': 'Work experience added successfully'})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def edit_work_experience(request, pk):
    """Edit work experience entry"""
    work = get_object_or_404(WorkExperience, pk=pk, user=request.user)
    
    if request.method == 'GET':
        return JsonResponse({
            'id': work.id,
            'job_title': work.job_title,
            'company': work.company,
            'location': work.location,
            'start_date': work.start_date.isoformat(),
            'end_date': work.end_date.isoformat() if work.end_date else None,
            'current': work.current,
            'description': work.description
        })
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = WorkExperienceForm(data, instance=work)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Work experience updated successfully'})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def delete_work_experience(request, pk):
    """Delete work experience entry"""
    work = get_object_or_404(WorkExperience, pk=pk, user=request.user)
    if request.method == 'DELETE':
        work.delete()
        return JsonResponse({'success': True, 'message': 'Work experience deleted successfully'})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


# Skills Views
@login_required
def add_skill(request):
    """Add skill"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = SkillForm(data)
            if form.is_valid():
                skill = form.save(commit=False)
                skill.user = request.user
                skill.save()
                return JsonResponse({'success': True, 'message': 'Skill added successfully'})
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def delete_skill(request, pk):
    """Delete skill"""
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'DELETE':
        skill.delete()
        return JsonResponse({'success': True, 'message': 'Skill deleted successfully'})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)