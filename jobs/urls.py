from django.urls import path
from . import views

urlpatterns = [

    # Recruiter job management
    path('', views.JobListView.as_view(), name='job_list'),
    path('post/', views.PostJobView.as_view(), name='post_job'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('<int:pk>/edit/', views.EditJobView.as_view(), name='edit_job'),
    path('<int:pk>/delete/', views.DeleteJobView.as_view(), name='delete_job'),
    path('my-jobs/', views.RecruiterJobListView.as_view(), name='recruiter_jobs'),

    # Google Talent integration endpoints
    path('google/search/', views.google_search, name='google_search'),
    path('google/autocomplete/', views.google_autocomplete, name='google_autocomplete'),
    path('google/job/<path:external_id>/', views.google_job_detail, name='google_job_detail'),
]