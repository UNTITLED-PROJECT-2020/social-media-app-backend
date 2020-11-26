# Generated by Django 3.0.3 on 2020-11-25 10:18

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_group_groupmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialogue',
            name='last_received_receiver',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 11, 25, 15, 48, 10, 532634)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dialogue',
            name='last_seen_receiver',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 11, 25, 15, 48, 33, 764092)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='bio',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Group Bio'),
        ),
        migrations.AlterField(
            model_name='groupmessage',
            name='command',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='message',
            name='command',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='dialogue',
            unique_together={('sender', 'receiver')},
        ),
    ]
