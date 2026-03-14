from django.contrib import admin
from django.urls import path
from django.urls import include
from jobs import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-portal/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('jobs/', include('jobs.urls')),
    path('companies/', include('companies.urls')),
    path('accounts/', include('accounts.urls')), 
    path('applications/', include('applications.urls')),
]
