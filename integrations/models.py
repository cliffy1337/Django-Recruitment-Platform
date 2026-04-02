 # Store external job mappings and sync status
from django.db import models
from django.conf import settings

class ExternalJobBoard(models.Model):
    """Registry of external job boards (Google, Indeed, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    adapter_class = models.CharField(max_length=255)  # e.g., 'integrations.google_talent.GoogleTalentAdapter'
    is_active = models.BooleanField(default=True)
    config = models.JSONField(default=dict, blank=True)  # API keys, endpoints, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ExternalJobMapping(models.Model):
    """Links a local Job to an external job board's ID."""
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='external_mappings')
    board = models.ForeignKey(ExternalJobBoard, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=255)  # Google's full resource name
    external_data = models.JSONField(default=dict, blank=True)  # Snapshot of external job data
    last_synced = models.DateTimeField(auto_now=True)
    sync_status = models.CharField(max_length=50, default='pending',
                                   choices=[('pending', 'Pending'),
                                            ('synced', 'Synced'),
                                            ('failed', 'Failed')])

    class Meta:
        unique_together = ('job', 'board')

    def __str__(self):
        return f"{self.job} -> {self.board} ({self.external_id})"
