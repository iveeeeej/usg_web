from django.db import migrations, models


def normalize_removed_announcement_types(apps, schema_editor):
    Announcement = apps.get_model('announcements', 'Announcement')
    Announcement.objects.filter(announcement_type='meeting').update(announcement_type='event')
    Announcement.objects.filter(announcement_type='workshop').update(announcement_type='seminar')


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0002_announcement_announcement_type_and_status_default'),
    ]

    operations = [
        migrations.RunPython(
            normalize_removed_announcement_types,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='announcement_type',
            field=models.CharField(
                choices=[
                    ('event', 'Event'),
                    ('cleaning', 'Cleaning'),
                    ('seminar', 'Seminar'),
                    ('maintenance', 'Maintenance'),
                    ('urgent', 'Urgent'),
                    ('important', 'Important'),
                ],
                db_index=True,
                max_length=24,
            ),
        ),
    ]
