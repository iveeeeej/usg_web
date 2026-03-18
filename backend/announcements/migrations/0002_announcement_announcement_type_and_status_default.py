from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='announcement_type',
            field=models.CharField(
                choices=[
                    ('event', 'Event'),
                    ('cleaning', 'Cleaning'),
                    ('meeting', 'Meeting'),
                    ('seminar', 'Seminar'),
                    ('workshop', 'Workshop'),
                    ('maintenance', 'Maintenance'),
                    ('urgent', 'Urgent'),
                    ('important', 'Important'),
                ],
                db_index=True,
                default='important',
                max_length=24,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='status',
            field=models.CharField(
                choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published'), ('ARCHIVED', 'Archived')],
                db_index=True,
                default='PUBLISHED',
                max_length=16,
            ),
        ),
    ]
