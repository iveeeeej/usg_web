from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Event, EventAttachment
from .permissions import IsOfficerOrReadOnly
from .serializers import EventAttachmentSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOfficerOrReadOnly]

    def get_queryset(self):
        queryset = Event.objects.select_related('created_by').all()

        if self.request.user.role != 'OFFICER':
            queryset = queryset.filter(status=Event.PUBLISHED)

        status_value = self.request.query_params.get('status')
        event_type = self.request.query_params.get('event_type')
        audience_scope = self.request.query_params.get('audience_scope')
        upcoming = self.request.query_params.get('upcoming')
        ordering = self.request.query_params.get('ordering')

        if status_value:
            queryset = queryset.filter(status=status_value)

        if event_type:
            queryset = queryset.filter(event_type=event_type)

        if audience_scope:
            queryset = queryset.filter(audience_scope=audience_scope)

        if upcoming == 'true':
            queryset = queryset.filter(end_datetime__gte=timezone.now())
        elif upcoming == 'false':
            queryset = queryset.filter(end_datetime__lt=timezone.now())

        if ordering in {'start_datetime', '-start_datetime', 'created_at', '-created_at'}:
            queryset = queryset.order_by(ordering)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EventAttachmentListCreateView(generics.ListCreateAPIView):
    serializer_class = EventAttachmentSerializer
    permission_classes = [IsAuthenticated, IsOfficerOrReadOnly]

    def get_event(self):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        if self.request.user.role != 'OFFICER' and event.status != Event.PUBLISHED:
            raise Http404
        return event

    def get_queryset(self):
        event = self.get_event()
        return EventAttachment.objects.filter(event=event).select_related('event', 'uploaded_by')

    def perform_create(self, serializer):
        serializer.save(event=self.get_event(), uploaded_by=self.request.user)


class EventAttachmentDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = EventAttachmentSerializer
    permission_classes = [IsAuthenticated, IsOfficerOrReadOnly]

    def get_queryset(self):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        queryset = EventAttachment.objects.filter(event=event).select_related('event', 'uploaded_by')
        if self.request.user.role != 'OFFICER':
            queryset = queryset.filter(event__status=Event.PUBLISHED)
        return queryset
