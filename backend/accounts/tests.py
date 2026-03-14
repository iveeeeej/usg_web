from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from announcements.models import Announcement
from events.models import Event
from .models import User


class UserModelTests(TestCase):
    def test_create_user_persists_profile_fields(self):
        user = User.objects.create_user(
            student_id='2026-0001',
            email='student@example.com',
            password='secure-password',
            role='STUDENT',
            first_name='Jamie',
            middle_name='Reyes',
            last_name='Santiago',
            year_level=3,
            section='A',
            course='BSIT',
        )

        self.assertEqual(user.first_name, 'Jamie')
        self.assertEqual(user.middle_name, 'Reyes')
        self.assertEqual(user.last_name, 'Santiago')
        self.assertEqual(user.year_level, 3)
        self.assertEqual(user.section, 'A')
        self.assertEqual(user.course, 'BSIT')
        self.assertIsNotNone(user.updated_at)

    def test_get_full_name_omits_missing_middle_name(self):
        user = User.objects.create_user(
            student_id='2026-0002',
            email='officer@example.com',
            password='secure-password',
            role='OFFICER',
            first_name='Alex',
            last_name='Rivera',
        )

        self.assertEqual(user.get_full_name(), 'Alex Rivera')


class AdminDashboardViewTests(APITestCase):
    def setUp(self):
        self.officer = User.objects.create_user(
            student_id='2026-9001',
            email='dashboard-officer@example.com',
            password='secure-password',
            role='OFFICER',
            position='PIO',
            first_name='Taylor',
            last_name='Officer',
        )
        self.student = User.objects.create_user(
            student_id='2026-9002',
            email='dashboard-student@example.com',
            password='secure-password',
            role='STUDENT',
            first_name='Jordan',
            last_name='Student',
        )

    def test_officer_dashboard_returns_live_stats(self):
        Event.objects.create(
            title='Upcoming Event',
            description='Upcoming',
            event_type=Event.EVENT,
            start_datetime=timezone.now() + timedelta(days=1),
            end_datetime=timezone.now() + timedelta(days=1, hours=2),
            venue='Gym',
            status=Event.PUBLISHED,
            audience_scope=Event.ORGANIZATION_WIDE,
            created_by=self.officer,
        )
        Event.objects.create(
            title='Past Event',
            description='Past',
            event_type=Event.EVENT,
            start_datetime=timezone.now() - timedelta(days=2),
            end_datetime=timezone.now() - timedelta(days=2, hours=-1),
            venue='Conference Room',
            status=Event.ARCHIVED,
            audience_scope=Event.ORGANIZATION_WIDE,
            created_by=self.officer,
        )
        Announcement.objects.create(
            title='Published Announcement',
            content='Visible update.',
            status=Announcement.PUBLISHED,
            created_by=self.officer,
        )
        Announcement.objects.create(
            title='Draft Announcement',
            content='Draft update.',
            status=Announcement.DRAFT,
            created_by=self.officer,
        )

        self.client.force_authenticate(user=self.officer)
        response = self.client.get('/api/officer/dashboard/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['officer']['name'], 'Taylor Officer')
        self.assertEqual(response.data['stats']['total_events'], 2)
        self.assertEqual(response.data['stats']['upcoming_events'], 1)
        self.assertEqual(response.data['stats']['published_announcements'], 1)
        self.assertEqual(response.data['stats']['draft_announcements'], 1)
        self.assertEqual(len(response.data['recent_announcements']), 2)
        returned_titles = {
            announcement['title'] for announcement in response.data['recent_announcements']
        }
        self.assertSetEqual(
            returned_titles,
            {'Published Announcement', 'Draft Announcement'},
        )

    def test_student_cannot_access_officer_dashboard(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.get('/api/officer/dashboard/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
