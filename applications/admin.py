from django.contrib import admin
from .models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'user', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'user__email', 'user__username')
    list_select_related = ('job', 'user')
    raw_id_fields = ('job', 'user')
    readonly_fields = ('applied_at', 'updated_at')
    
    fieldsets = (
        ('Application', {
            'fields': ('job', 'user', 'status')
        }),
        ('Documents', {
            'fields': ('resume', 'cover_letter_file', 'cover_letter_text', 'portfolio')
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )