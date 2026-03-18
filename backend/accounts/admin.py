from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DashboardMessage, User


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        'student_id',
        'email',
        'first_name',
        'last_name',
        'role',
        'year_level',
        'is_staff',
        'is_active',
    )
    list_filter = ('role', 'year_level', 'is_staff', 'is_active')
    readonly_fields = ('last_login', 'created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('student_id', 'email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'middle_name', 'last_name')}),
        ('Academic Information', {'fields': ('year_level', 'section', 'course')}),
        ('Role Information', {'fields': ('role', 'position')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'student_id',
                'email',
                'first_name',
                'middle_name',
                'last_name',
                'role',
                'position',
                'year_level',
                'section',
                'course',
                'password1',
                'password2',
                'is_staff',
                'is_active',
            )}
        ),
    )

    search_fields = ('student_id', 'email', 'first_name', 'last_name', 'course', 'section')
    ordering = ('student_id',)


admin.site.register(User, CustomUserAdmin)


@admin.register(DashboardMessage)
class DashboardMessageAdmin(admin.ModelAdmin):
    list_display = ('key', 'short_message', 'updated_by', 'updated_at')
    readonly_fields = ('key', 'created_at', 'updated_at')
    search_fields = ('message',)

    def short_message(self, obj):
        preview = obj.message.strip().splitlines()[0] if obj.message else ''
        return preview[:80]

    short_message.short_description = 'Message'
