from django.utils import timezone
from rest_framework import serializers

from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = (
            'id',
            'title',
            'announcement_type',
            'content',
            'status',
            'published_at',
            'created_by',
            'created_by_name',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('published_at', 'created_by', 'created_at', 'updated_at')

    def get_created_by_name(self, obj):
        full_name = obj.created_by.get_full_name()
        return full_name or obj.created_by.student_id

    def create(self, validated_data):
        if validated_data.get('status') == Announcement.PUBLISHED:
            validated_data.setdefault('published_at', timezone.now())
        return super().create(validated_data)

    def update(self, instance, validated_data):
        status = validated_data.get('status', instance.status)
        if status == Announcement.PUBLISHED and instance.published_at is None:
            validated_data.setdefault('published_at', timezone.now())
        return super().update(instance, validated_data)
