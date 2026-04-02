# applications/models.py
from django.db import models
from django.conf import settings
from config.storage_backends import ResumeStorage, ApplicationDocumentStorage
# Import other necessary modules

class JobApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    
    # Resume uploaded for this application
    resume = models.FileField(
        upload_to='applications/%Y/%m/%d/',
        storage=ResumeStorage(),
        blank=True,
        null=True,
        verbose_name='Resume'
    )
    
    # Cover letter file (optional)
    cover_letter_file = models.FileField(
        upload_to='cover_letters/%Y/%m/%d/',
        storage=ApplicationDocumentStorage(),
        blank=True,
        null=True,
        verbose_name='Cover Letter File'
    )
    
    # Cover letter text
    cover_letter_text = models.TextField(
        blank=True,
        null=True,
        verbose_name='Cover Letter Text'
    )
    
    # Additional documents
    portfolio = models.FileField(
        upload_to='portfolios/%Y/%m/%d/',
        storage=ApplicationDocumentStorage(),
        blank=True,
        null=True,
        verbose_name='Portfolio'
    )
    
    # Application status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.job.title}"