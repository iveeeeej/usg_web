from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsOfficer
from accounts.serializers import DashboardMessageSerializer
from announcements.models import Announcement
from events.models import Event
from .models import DashboardMessage


def get_dashboard_message():
    dashboard_message, _ = DashboardMessage.objects.get_or_create(
        key=DashboardMessage.WHATS_NEW,
        defaults={'message': DashboardMessage.DEFAULT_MESSAGE},
    )
    return DashboardMessage.objects.select_related('updated_by').get(pk=dashboard_message.pk)


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsOfficer]

    def get(self, request):
        dashboard_message = get_dashboard_message()
        recent_announcements = (
            Announcement.objects.select_related('created_by')
            .annotate(sort_datetime=Coalesce('published_at', 'created_at'))
            .order_by('-sort_datetime')[:5]
        )
        now = timezone.now()

        return Response(
            {
                "officer": {
                    "student_id": request.user.student_id,
                    "name": request.user.get_full_name(),
                    "position": request.user.position,
                },
                "dashboard_message": DashboardMessageSerializer(dashboard_message).data,
                "stats": {
                    "total_events": Event.objects.count(),
                    "upcoming_events": Event.objects.filter(end_datetime__gte=now).count(),
                    "published_announcements": Announcement.objects.filter(
                        status=Announcement.PUBLISHED
                    ).count(),
                    "draft_announcements": Announcement.objects.filter(
                        status=Announcement.DRAFT
                    ).count(),
                },
                "recent_announcements": [
                    {
                        "id": str(announcement.id),
                        "title": announcement.title,
                        "content": announcement.content,
                        "status": announcement.status,
                        "published_at": announcement.published_at,
                        "created_at": announcement.created_at,
                        "created_by": announcement.created_by.get_full_name(),
                    }
                    for announcement in recent_announcements
                ],
            }
        )


class DashboardMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in {'PATCH', 'PUT'}:
            return [IsAuthenticated(), IsOfficer()]
        return [IsAuthenticated()]

    def get(self, request):
        serializer = DashboardMessageSerializer(get_dashboard_message())
        return Response(serializer.data)

    def patch(self, request):
        dashboard_message = get_dashboard_message()
        serializer = DashboardMessageSerializer(
            dashboard_message,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        dashboard_message.refresh_from_db()
        return Response(DashboardMessageSerializer(dashboard_message).data)
