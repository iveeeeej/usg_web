from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from .models import Announcement


class AnnouncementApiTests(APITestCase):
    def setUp(self):
        self.officer = User.objects.create_user(
            student_id='2026-3000',
            email='announcements-officer@example.com',
            password='secure-password',
            role='OFFICER',
            first_name='Casey',
            last_name='Officer',
        )
        self.student = User.objects.create_user(
            student_id='2026-4000',
            email='announcements-student@example.com',
            password='secure-password',
            role='STUDENT',
            first_name='Drew',
            last_name='Student',
        )
        self.base_payload = {
            'title': 'Enrollment Advisory',
            'announcement_type': Announcement.TYPE_IMPORTANT,
            'content': 'Enrollment support desk will open at 8 AM.',
        }

    def test_officer_can_create_announcement(self):
        self.client.force_authenticate(user=self.officer)

        response = self.client.post('/api/announcements/', self.base_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['created_by_name'], 'Casey Officer')
        self.assertEqual(response.data['announcement_type'], Announcement.TYPE_IMPORTANT)
        self.assertEqual(Announcement.objects.count(), 1)
        created_announcement = Announcement.objects.get()
        self.assertEqual(created_announcement.created_by, self.officer)
        self.assertEqual(created_announcement.status, Announcement.PUBLISHED)
        self.assertIsNotNone(created_announcement.published_at)

    def test_student_cannot_create_announcement(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.post('/api/announcements/', self.base_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_officer_create_requires_announcement_type(self):
        self.client.force_authenticate(user=self.officer)

        invalid_payload = {
            'title': 'Missing type',
            'content': 'This should fail validation.',
        }

        response = self.client.post('/api/announcements/', invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('announcement_type', response.data)

    def test_removed_announcement_types_are_rejected(self):
        self.client.force_authenticate(user=self.officer)

        invalid_payload = {
            'title': 'Old category',
            'announcement_type': 'meeting',
            'content': 'This should fail validation.',
        }

        response = self.client.post('/api/announcements/', invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('announcement_type', response.data)

    def test_officer_can_update_announcement(self):
        announcement = Announcement.objects.create(
            title='Original Announcement',
            announcement_type=Announcement.TYPE_EVENT,
            content='Initial content.',
            status=Announcement.PUBLISHED,
            created_by=self.officer,
        )
        self.client.force_authenticate(user=self.officer)

        response = self.client.patch(
            f'/api/announcements/{announcement.id}/',
            {
                'title': 'Updated Announcement',
                'content': 'Updated content.',
                'announcement_type': Announcement.TYPE_IMPORTANT,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        announcement.refresh_from_db()
        self.assertEqual(announcement.title, 'Updated Announcement')
        self.assertEqual(announcement.content, 'Updated content.')
        self.assertEqual(announcement.announcement_type, Announcement.TYPE_IMPORTANT)

    def test_officer_can_delete_announcement(self):
        announcement = Announcement.objects.create(
            title='Delete Me',
            announcement_type=Announcement.TYPE_EVENT,
            content='Temporary content.',
            status=Announcement.PUBLISHED,
            created_by=self.officer,
        )
        self.client.force_authenticate(user=self.officer)

        response = self.client.delete(f'/api/announcements/{announcement.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Announcement.objects.filter(id=announcement.id).exists())

    def test_student_only_sees_published_announcements(self):
        Announcement.objects.create(
            title='Published Announcement',
            announcement_type=Announcement.TYPE_EVENT,
            content='Visible to students.',
            status=Announcement.PUBLISHED,
            created_by=self.officer,
        )
        Announcement.objects.create(
            title='Draft Announcement',
            announcement_type=Announcement.TYPE_IMPORTANT,
            content='Officer only.',
            status=Announcement.DRAFT,
            created_by=self.officer,
        )
        self.client.force_authenticate(user=self.student)

        response = self.client.get('/api/announcements/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Published Announcement')
        self.assertEqual(response.data[0]['created_by_name'], 'Casey Officer')
        self.assertEqual(response.data[0]['announcement_type'], Announcement.TYPE_EVENT)
