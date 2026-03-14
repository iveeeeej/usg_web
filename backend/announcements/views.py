from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Announcement
from .permissions import IsOfficerOrReadOnly
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated, IsOfficerOrReadOnly]

    def get_queryset(self):
        queryset = Announcement.objects.select_related('created_by').all()

        if self.request.user.role != 'OFFICER':
            queryset = queryset.filter(status=Announcement.PUBLISHED)

        status_value = self.request.query_params.get('status')
        ordering = self.request.query_params.get('ordering')

        if status_value:
            queryset = queryset.filter(status=status_value)

        if ordering in {'published_at', '-published_at', 'created_at', '-created_at'}:
            queryset = queryset.order_by(ordering)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
