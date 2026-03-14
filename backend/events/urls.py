from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventAttachmentDetailView, EventAttachmentListCreateView, EventViewSet

router = DefaultRouter()
router.register('events', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'events/<uuid:event_id>/attachments/',
        EventAttachmentListCreateView.as_view(),
        name='event-attachment-list',
    ),
    path(
        'events/<uuid:event_id>/attachments/<uuid:pk>/',
        EventAttachmentDetailView.as_view(),
        name='event-attachment-detail',
    ),
]
