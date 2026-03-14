from django.contrib import admin

from .models import Event, EventAttachment


class EventAttachmentInline(admin.TabularInline):
    model = EventAttachment
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'event_type',
        'status',
        'audience_scope',
        'start_datetime',
        'end_datetime',
        'venue',
        'created_by',
    )
    list_filter = ('event_type', 'status', 'audience_scope')
    search_fields = ('title', 'venue', 'audience_label', 'created_by__student_id')
    ordering = ('start_datetime',)
    readonly_fields = ('published_at', 'created_at', 'updated_at')
    inlines = [EventAttachmentInline]


@admin.register(EventAttachment)
class EventAttachmentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'event', 'file_type', 'uploaded_by', 'created_at')
    list_filter = ('file_type',)
    search_fields = ('file_name', 'event__title', 'uploaded_by__student_id')
    ordering = ('created_at',)
    readonly_fields = ('created_at',)
