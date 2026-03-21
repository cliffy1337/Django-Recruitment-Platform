from django.contrib import admin
from django.urls import path, include
from jobs import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('admin-portal/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('jobs/', include('jobs.urls')),
    path('companies/', include('companies.urls')),
    path('accounts/', include('accounts.urls')), 
    path('applications/', include('applications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)