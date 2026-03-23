from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from config.storage_backends import ProfilePictureStorage, ResumeStorage

class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    Compatible with django-allauth.
    """
    
    # Add any additional fields you need
    profile_picture = models.ImageField(
        upload_to='profile_pictures/%Y/%m/%d/',
        storage=ProfilePictureStorage(),
        blank=True,
        null=True,
        verbose_name=_('Profile Picture')
    )
    
    resume = models.FileField(
        upload_to='resumes/%Y/%m/%d/',
        storage=ResumeStorage(),
        blank=True,
        null=True,
        verbose_name=_('Resume/CV')
    )
    
    # User type for job portal
    USER_TYPE_CHOICES = [
        ('job_seeker', _('Job Seeker')),
        ('recruiter', _('Recruiter')),
        ('admin', _('Admin')),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='job_seeker',
        verbose_name=_('User Type')
    )
    
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name=_('Phone Number')
    )
    
    company_name = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name=_('Company Name')  # For recruiters
    )
    
    # Track if user has completed onboarding
    onboarding_completed = models.BooleanField(
        default=False,
        verbose_name=_('Onboarding Completed')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        # Add this to avoid any permission conflicts
        swappable = 'AUTH_USER_MODEL'
    
    def __str__(self):
        return self.email or self.username
    
    @property
    def is_recruiter(self):
        return self.user_type == 'recruiter'
    
    @property
    def is_job_seeker(self):
        return self.user_type == 'job_seeker'