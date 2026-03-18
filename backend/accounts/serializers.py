from rest_framework import serializers

from .models import DashboardMessage


class DashboardMessageSerializer(serializers.ModelSerializer):
    updated_by_name = serializers.SerializerMethodField()

    class Meta:
        model = DashboardMessage
        fields = (
            'key',
            'message',
            'updated_at',
            'updated_by',
            'updated_by_name',
        )
        read_only_fields = ('key', 'updated_at', 'updated_by', 'updated_by_name')

    def get_updated_by_name(self, obj):
        if not obj.updated_by:
            return None

        full_name = obj.updated_by.get_full_name()
        return full_name or obj.updated_by.student_id
