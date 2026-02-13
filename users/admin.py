from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'role', 'email_verified', 'is_locked', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'email_verified', 'is_locked')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'email_verified', 'is_2fa_enabled', 'is_locked', 'failed_login_attempts')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'email_verified', 'is_2fa_enabled')}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'get_rank', 'streak', 'language_preference')
    search_fields = ('user__username', 'user__email')
