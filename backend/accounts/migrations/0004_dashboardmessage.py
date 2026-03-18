import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_add_user_profile_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default='whats_new', editable=False, max_length=50, unique=True)),
                ('message', models.TextField(default='Welcome to a new school year!')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_dashboard_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dashboard message',
                'verbose_name_plural': 'Dashboard messages',
            },
        ),
    ]
