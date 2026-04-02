from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class CustomUserAdmin(UserAdmin):
    """
    Custom admin for User model with allauth integration
    """
    
    # Fields to display in list view
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active', 'onboarding_completed')
    list_filter = ('user_type', 'is_staff', 'is_active', 'onboarding_completed')
    search_fields = ('username', 'email', 'phone', 'company_name')
    
    # Fields to display in detail view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': (
            'email', 
            'first_name', 
            'last_name', 
            'phone',
            'profile_picture',
            'resume'
        )}),
        (_('Account Type'), {'fields': ('user_type', 'company_name', 'onboarding_completed')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    
    # Fields for creating new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )
    
    # Readonly fields
    readonly_fields = ('created_at', 'updated_at')
    
    # Ordering
    ordering = ('-date_joined',)

# Register the custom user model
admin.site.register(User, CustomUserAdmin)