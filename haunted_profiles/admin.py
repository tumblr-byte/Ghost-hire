from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model"""
    
    list_display = ['username', 'email', 'is_verified', 'ghost_level', 'created_at', 'is_staff']
    list_filter = ['is_verified', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email', 'google_id']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'google_id', 'bio', 'github_link')}),
        ('Ghost Profile', {'fields': ('ghost_avatar', 'ghost_level', 'skills', 'is_verified')}),
        ('Verification', {'fields': ('verification_photo',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at')}),
    )
    
    readonly_fields = ['created_at', 'last_login']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
