import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_is_verified_remove_user_verified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='course',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='middle_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='section',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='year_level',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
