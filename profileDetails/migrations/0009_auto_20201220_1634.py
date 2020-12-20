# Generated by Django 3.1.1 on 2020-12-20 11:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('environments', '0006_auto_20201112_0228'),
        ('profileDetails', '0008_auto_20201215_1752'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ledger',
            options={'ordering': ('account', 'score', 'created')},
        ),
        migrations.RenameField(
            model_name='accountdetail',
            old_name='Account',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='ledger',
            old_name='account',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='ledger',
            old_name='env',
            new_name='env',
        ),
        migrations.AlterUniqueTogether(
            name='ledger',
            unique_together={('env', 'account')},
        ),
    ]
