# Generated by Django 5.1.6 on 2025-03-03 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_delete_participant_event_asset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='asset',
            field=models.ImageField(blank=True, default='events_asset/default_img.jpg', null=True, upload_to='events_asset'),
        ),
    ]
