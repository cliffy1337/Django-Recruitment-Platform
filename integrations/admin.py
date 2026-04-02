from django.contrib import admin
from .models import ExternalJobBoard, ExternalJobMapping

@admin.register(ExternalJobBoard)
class ExternalJobBoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'adapter_class', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'adapter_class')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Board Information', {
            'fields': ('name', 'adapter_class', 'is_active')
        }),
        ('Configuration', {
            'fields': ('config',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

@admin.register(ExternalJobMapping)
class ExternalJobMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'board', 'external_id', 'sync_status', 'last_synced')
    list_filter = ('sync_status', 'board', 'last_synced')
    search_fields = ('job__title', 'external_id')
    raw_id_fields = ('job',)
    readonly_fields = ('last_synced',)
    
    fieldsets = (
        ('Mapping', {
            'fields': ('job', 'board', 'external_id')
        }),
        ('Sync Information', {
            'fields': ('sync_status', 'external_data', 'last_synced')
        }),
    )