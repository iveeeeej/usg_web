from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0003_remove_meeting_and_workshop_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='announcement_type',
            field=models.CharField(
                choices=[
                    ('general', 'General'),
                    ('event', 'Event'),
                    ('academic', 'Academic'),
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
