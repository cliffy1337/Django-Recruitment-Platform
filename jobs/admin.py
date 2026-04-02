from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'location', 'employment_type', 'status', 'created_at')
    list_filter = ('status', 'employment_type', 'is_remote', 'is_featured', 'created_at')
    search_fields = ('title', 'company__name', 'location')
    list_select_related = ('company',)
    raw_id_fields = ('company',)
    readonly_fields = ('views_count', 'applications_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company', 'title', 'description', 'requirements')
        }),
        ('Location & Type', {
            'fields': ('location', 'is_remote', 'employment_type')
        }),
        ('Compensation', {
            'fields': ('salary_min', 'salary_max')
        }),
        ('Status & Visibility', {
            'fields': ('status', 'is_featured')
        }),
        ('Application Settings', {
            'fields': ('apply_url',)
        }),
        ('External Sync', {
            'fields': ('synced_to_google', 'google_job_id'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views_count', 'applications_count'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )