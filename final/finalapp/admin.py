from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from .form import CustomUserChangeForm


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'role', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'phone_number'),
        }),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'phone_number')
    search_fields = ('username', 'email', 'role', 'phone_number')
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Hiring)
admin.site.register(completed_jobs)
""" admin.site.register(job_selected) """
