from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_applications, name='my_applications'),
]