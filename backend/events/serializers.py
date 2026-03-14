from django.utils import timezone
from rest_framework import serializers

from .models import Event, EventAttachment


class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'event_type',
            'start_datetime',
            'end_datetime',
            'venue',
            'status',
            'audience_scope',
            'audience_label',
            'created_by',
            'published_at',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_by', 'published_at', 'created_at', 'updated_at')

    def validate(self, attrs):
        start_datetime = attrs.get('start_datetime', getattr(self.instance, 'start_datetime', None))
        end_datetime = attrs.get('end_datetime', getattr(self.instance, 'end_datetime', None))
        audience_scope = attrs.get('audience_scope', getattr(self.instance, 'audience_scope', None))
        audience_label = attrs.get('audience_label', getattr(self.instance, 'audience_label', None))

        if start_datetime and end_datetime and end_datetime <= start_datetime:
            raise serializers.ValidationError({
                'end_datetime': 'End datetime must be after start datetime.'
            })

        if audience_scope == Event.INTERNAL and not audience_label:
            raise serializers.ValidationError({
                'audience_label': 'Audience label is required for internal events.'
            })

        return attrs

    def create(self, validated_data):
        if validated_data.get('status') == Event.PUBLISHED:
            validated_data.setdefault('published_at', timezone.now())
        return super().create(validated_data)

    def update(self, instance, validated_data):
        status = validated_data.get('status', instance.status)
        if status == Event.PUBLISHED and instance.published_at is None:
            validated_data.setdefault('published_at', timezone.now())
        return super().update(instance, validated_data)


class EventAttachmentSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(read_only=True)
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = EventAttachment
        fields = (
            'id',
            'event',
            'file_name',
            'file_path',
            'file_type',
            'uploaded_by',
            'created_at',
        )
        read_only_fields = ('event', 'uploaded_by', 'created_at')
