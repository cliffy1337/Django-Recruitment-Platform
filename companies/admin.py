from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'location', 'verified', 'created_at')
    list_filter = ('verified', 'created_at')
    search_fields = ('name', 'user__email', 'user__username', 'location')
    raw_id_fields = ('user',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'name')
        }),
        ('Details', {
            'fields': ('description', 'website', 'location')
        }),
        ('Verification', {
            'fields': ('logo', 'verified')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )