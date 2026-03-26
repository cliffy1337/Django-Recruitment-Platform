from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/upload-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('profile/delete-picture/', views.delete_profile_picture, name='delete_profile_picture'),
    path('profile/upload-resume/', views.upload_resume, name='upload_resume'),
    path('profile/delete-resume/', views.delete_resume, name='delete_resume'),
    
    # Education URLs
    path('profile/education/add/', views.add_education, name='add_education'),
    path('profile/education/edit/<int:pk>/', views.edit_education, name='edit_education'),
    path('profile/education/delete/<int:pk>/', views.delete_education, name='delete_education'),
    
    # Work Experience URLs
    path('profile/work/add/', views.add_work_experience, name='add_work_experience'),
    path('profile/work/edit/<int:pk>/', views.edit_work_experience, name='edit_work_experience'),
    path('profile/work/delete/<int:pk>/', views.delete_work_experience, name='delete_work_experience'),
    
    # Skills URLs
    path('profile/skill/add/', views.add_skill, name='add_skill'),
    path('profile/skill/delete/<int:pk>/', views.delete_skill, name='delete_skill'),
]