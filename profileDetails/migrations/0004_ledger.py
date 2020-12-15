# Generated by Django 3.1.1 on 2020-12-07 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('environments', '0006_auto_20201112_0228'),
        ('profileDetails', '0003_auto_20201107_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('Env_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='environments.environments')),
                ('User_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('Env_FK', 'score', 'created'),
                'unique_together': {('Env_FK', 'User_FK')},
            },
        ),
    ]
