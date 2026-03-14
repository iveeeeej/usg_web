from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from .models import Event


class EventApiTests(APITestCase):
    def setUp(self):
        self.officer = User.objects.create_user(
            student_id='2026-1000',
            email='officer@example.com',
            password='secure-password',
            role='OFFICER',
            first_name='Avery',
            last_name='Officer',
        )
        self.student = User.objects.create_user(
            student_id='2026-2000',
            email='student@example.com',
            password='secure-password',
            role='STUDENT',
            first_name='Blake',
            last_name='Student',
        )
        self.base_payload = {
            'title': 'USG Assembly',
            'description': 'Semester-wide assembly update',
            'event_type': Event.GENERAL_ASSEMBLY,
            'start_datetime': (timezone.now() + timedelta(days=1)).isoformat(),
            'end_datetime': (timezone.now() + timedelta(days=1, hours=2)).isoformat(),
            'venue': 'Main Auditorium',
            'status': Event.PUBLISHED,
            'audience_scope': Event.ORGANIZATION_WIDE,
            'audience_label': '',
        }

    def test_officer_can_create_event(self):
        self.client.force_authenticate(user=self.officer)

        response = self.client.post('/api/events/', self.base_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().created_by, self.officer)
        self.assertIsNotNone(Event.objects.get().published_at)

    def test_student_cannot_create_event(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.post('/api/events/', self.base_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_only_sees_published_events(self):
        Event.objects.create(
            title='Published Event',
            description='Visible to students',
            event_type=Event.EVENT,
            start_datetime=timezone.now() + timedelta(days=2),
            end_datetime=timezone.now() + timedelta(days=2, hours=1),
            venue='Gym',
            status=Event.PUBLISHED,
            audience_scope=Event.ORGANIZATION_WIDE,
            created_by=self.officer,
        )
        Event.objects.create(
            title='Draft Event',
            description='Officer only',
            event_type=Event.EVENT,
            start_datetime=timezone.now() + timedelta(days=3),
            end_datetime=timezone.now() + timedelta(days=3, hours=1),
            venue='Conference Room',
            status=Event.DRAFT,
            audience_scope=Event.ORGANIZATION_WIDE,
            created_by=self.officer,
        )
        self.client.force_authenticate(user=self.student)

        response = self.client.get('/api/events/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Published Event')

    def test_internal_event_requires_audience_label(self):
        self.client.force_authenticate(user=self.officer)
        payload = {
            **self.base_payload,
            'status': Event.DRAFT,
            'audience_scope': Event.INTERNAL,
            'audience_label': '',
        }

        response = self.client.post('/api/events/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('audience_label', response.data)
