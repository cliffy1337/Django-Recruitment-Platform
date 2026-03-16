from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Job
from .forms import JobForm
from .services import job_services
from companies.models import Company

def home(request):
    return render(request, 'jobs/index.html')

def job_list(request):
    return render(request, 'jobs/job_list.html')

def post_job(request):
    return render(request, 'jobs/post_job.html')

# ---------- Recruiter Job CRUD ----------

class RecruitorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'recruiter'

class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    queryset = Job.objects.filter(status='published')

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Increment view count
        self.object.views_count += 1
        self.object.save(update_fields=['views_count'])
        return response

class PostJobView(LoginRequiredMixin, RecruitorRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/post_job.html'
    success_url = reverse_lazy('recruiter_jobs')

    def form_valid(self, form):
        # Set the company from the recruiter's profile
        form.instance.company = Company.objects.get(user=self.request.user)
        form.instance.status = 'published'  # or 'draft' if you want moderation
        response = super().form_valid(form)
        # Optionally sync to Google automatically
        if form.cleaned_data.get('sync_to_google', False):
            job_services.sync_job_to_google(self.object)
        return response

class EditJobView(LoginRequiredMixin, RecruitorRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/edit_job.html'
    success_url = reverse_lazy('recruiter_jobs')

    def get_queryset(self):
        # Only allow editing jobs owned by the recruiter's company
        return Job.objects.filter(company__user=self.request.user)

class DeleteJobView(LoginRequiredMixin, RecruitorRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('recruiter_jobs')

    def get_queryset(self):
        return Job.objects.filter(company__user=self.request.user)

class RecruiterJobListView(LoginRequiredMixin, RecruitorRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/recruiter_dashboard.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(company__user=self.request.user)

# ---------- Google Talent Endpoints ----------

def google_search(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location')
    results = job_services.search_google_jobs(query, location)
    return render(request, 'jobs/google_search_results.html', {'jobs': results})

def google_autocomplete(request):
    query = request.GET.get('q', '')
    suggestions = job_services.autocomplete_google_query(query)
    return JsonResponse({'suggestions': suggestions})

def google_job_detail(request, external_id):
    job = job_services.get_google_job_details(external_id)
    # Track view event
    job_services.track_job_event('VIEW', external_id)
    return render(request, 'jobs/google_job_detail.html', {'job': job})

