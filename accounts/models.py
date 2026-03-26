from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from config.storage_backends import ProfilePictureStorage, ResumeStorage


class User(AbstractUser):
    """
    Custom User model for a job portal.
    Extends AbstractUser, compatible with django-allauth.
    Uses email as the primary login field.
    """

    email = models.EmailField(_('Email Address'), unique=True)

    # Profile picture and resume with custom storage
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
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        verbose_name=_('Resume/CV')
    )

    # User type
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

    # Optional fields
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone Number'))
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Company Name'))

    # Onboarding tracking
    onboarding_completed = models.BooleanField(default=False, verbose_name=_('Onboarding Completed'))

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email as primary login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username is still required by AbstractUser

    class Meta:
        db_table = 'accounts_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email or self.username

    @property
    def is_recruiter(self):
        return self.user_type == 'recruiter'

    @property
    def is_job_seeker(self):
        return self.user_type == 'job_seeker'

    @property
    def profile_picture_url(self):
        """Return profile picture URL or fallback"""
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return '/static/images/default-avatar.png'

    def delete_profile_picture(self):
        """Delete profile picture from storage"""
        if self.profile_picture:
            self.profile_picture.delete(save=False)
            self.profile_picture = None
            self.save(update_fields=['profile_picture'])
            return True
        return False

    def clean(self):
        """
        Model-level validation:
        - Company name is required if user is a recruiter.
        """
        super().clean()
        if self.is_recruiter and not self.company_name:
            raise ValidationError({
                'company_name': _('Company Name is required for recruiters.')
            })

    # Admin display helper
    def admin_profile_picture(self):
        if self.profile_picture:
            return format_html('<img src="{}" width="50" />', self.profile_picture.url)
        return ''
    admin_profile_picture.short_description = _('Profile Picture')

    # Add this at the end of your models.py file, after the User class

class Education(models.Model):
    """
    Education history for job seekers
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='education',
        verbose_name=_('User')
    )
    institution = models.CharField(max_length=255, verbose_name=_('Institution'))
    degree = models.CharField(max_length=255, verbose_name=_('Degree'))
    field_of_study = models.CharField(max_length=255, blank=True, verbose_name=_('Field of Study'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(blank=True, null=True, verbose_name=_('End Date'))
    current = models.BooleanField(default=False, verbose_name=_('Currently Studying'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_education'
        verbose_name = _('Education')
        verbose_name_plural = _('Education')
        ordering = ['-end_date', '-start_date']
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"


class WorkExperience(models.Model):
    """
    Work experience for job seekers
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='work_experience',
        verbose_name=_('User')
    )
    job_title = models.CharField(max_length=255, verbose_name=_('Job Title'))
    company = models.CharField(max_length=255, verbose_name=_('Company'))
    location = models.CharField(max_length=255, blank=True, verbose_name=_('Location'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(blank=True, null=True, verbose_name=_('End Date'))
    current = models.BooleanField(default=False, verbose_name=_('Currently Working'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_work_experience'
        verbose_name = _('Work Experience')
        verbose_name_plural = _('Work Experiences')
        ordering = ['-end_date', '-start_date']
    
    def __str__(self):
        return f"{self.job_title} at {self.company}"


class Skill(models.Model):
    """
    Skills for job seekers
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='skills',
        verbose_name=_('User')
    )
    name = models.CharField(max_length=100, verbose_name=_('Skill Name'))
    years_of_experience = models.PositiveIntegerField(default=0, verbose_name=_('Years of Experience'))
    
    class Meta:
        db_table = 'accounts_skill'
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        unique_together = ['user', 'name']
    
    def __str__(self):
        return self.name