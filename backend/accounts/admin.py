from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('student_id', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('student_id', 'email', 'password')}),
        ('Role Information', {'fields': ('role', 'position')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Verification', {'fields': ('is_verified', 'verified_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('student_id', 'email', 'password1', 'password2', 'role', 'position', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('student_id', 'email')
    ordering = ('student_id',)


admin.site.register(User, CustomUserAdmin)