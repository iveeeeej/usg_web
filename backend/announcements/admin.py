from django.contrib import admin

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'published_at', 'created_by', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'content', 'created_by__student_id')
    ordering = ('-published_at', '-created_at')
    readonly_fields = ('published_at', 'created_at', 'updated_at')
