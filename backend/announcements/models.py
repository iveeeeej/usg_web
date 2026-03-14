import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Announcement(models.Model):
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'
    ARCHIVED = 'ARCHIVED'
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (ARCHIVED, 'Archived'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=DRAFT, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_announcements',
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if self.status == self.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
