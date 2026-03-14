from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsOfficer
from announcements.models import Announcement
from events.models import Event


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsOfficer]

    def get(self, request):
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
