# Generated by Django 3.1.1 on 2020-10-28 22:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Environments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=20)),
                ('Description', models.CharField(max_length=300)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('User_Foreignkey', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
