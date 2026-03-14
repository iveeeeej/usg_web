import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Event(models.Model):
    EVENT = 'EVENT'
    GENERAL_ASSEMBLY = 'GENERAL_ASSEMBLY'
    EVENT_TYPE_CHOICES = (
        (EVENT, 'Event'),
        (GENERAL_ASSEMBLY, 'General Assembly'),
    )

    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'
    ARCHIVED = 'ARCHIVED'
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (ARCHIVED, 'Archived'),
    )

    ORGANIZATION_WIDE = 'ORGANIZATION_WIDE'
    INTERNAL = 'INTERNAL'
    AUDIENCE_SCOPE_CHOICES = (
        (ORGANIZATION_WIDE, 'Organization Wide'),
        (INTERNAL, 'Internal'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=32, choices=EVENT_TYPE_CHOICES, default=EVENT)
    start_datetime = models.DateTimeField(db_index=True)
    end_datetime = models.DateTimeField(db_index=True)
    venue = models.CharField(max_length=255)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=DRAFT, db_index=True)
    audience_scope = models.CharField(
        max_length=32,
        choices=AUDIENCE_SCOPE_CHOICES,
        default=ORGANIZATION_WIDE,
    )
    audience_label = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_events',
    )
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_datetime', 'created_at']

    def clean(self):
        if self.end_datetime <= self.start_datetime:
            raise ValidationError({'end_datetime': 'End datetime must be after start datetime.'})

        if self.audience_scope == self.INTERNAL and not self.audience_label:
            raise ValidationError({'audience_label': 'Audience label is required for internal events.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.status == self.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class EventAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attachments')
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    file_type = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='event_attachments',
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.event.title} - {self.file_name}"
