# Generated by Django 3.0.3 on 2020-12-18 12:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20201205_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='finished',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 19, 17, 43, 3, 947617)),
        ),
    ]
