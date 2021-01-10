# imports
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
# rest framework imports
from rest_framework.authtoken.models import Token

# Create your models here.

# ActiveDetail model for details about the activity of people
class ActiveDetail(models.Model):
    active = models.BooleanField(default=True)
    last_active = models.DateTimeField(null=True, blank=True)
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='activeDetail', verbose_name='user account', default=None)


# Dialogue model for a conversation between 2 people
class Dialogue(models.Model):  # dialogue model
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender', default=None)
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver', default=None)
    last_received_receiver = models.DateTimeField(auto_now_add=True)
    last_seen_receiver = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    class Meta:
        unique_together = ('sender', 'receiver',)

        ordering = ('receiver', '-last_seen_receiver',
                    '-last_received_receiver',)

# Message model for each message inside a Dialogue
class Message(models.Model):    # message model
    msg_from = models.CharField(
        max_length=10, verbose_name='Message From', blank=True, null=True)
    msg_to = models.CharField(
        max_length=10, verbose_name='Message To', blank=True, null=True)
    message = models.CharField(max_length=1200)
    command = models.CharField(max_length=20, default='')
    sent_timestamp = models.DateTimeField(
        null=True, blank=True, verbose_name='sent timestamp')
    dialogue = models.ForeignKey(
        Dialogue, on_delete=models.CASCADE, related_name='message',
        verbose_name='dialogue key', default=None)
    # received_timestamp = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.msg_from

    class Meta:
        ordering = ('msg_to', '-sent_timestamp',)


# Dialogue model for a conversation between multiple people
class Group(models.Model):    # Group model
    name = models.CharField(
        max_length=30, verbose_name='Group Name', blank=True, null=True)
    key = models.CharField(
        max_length=10, verbose_name='Group Key', unique=True, default=None)
    bio = models.CharField(
        max_length=80, verbose_name='Group Bio', blank=True, null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="participants",
                                          verbose_name='group participants', default=None)
    admin = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   verbose_name='group admins', default=None)

# Message model for each message inside a Dialogue
class GroupMessage(models.Model):    # Group Message model
    msg_from = models.CharField(
        max_length=10, verbose_name='Message From', default=None)
    msg_to = models.CharField(
        max_length=10, verbose_name='Message To', default=None)
    message = models.CharField(max_length=1200)
    command = models.CharField(max_length=20, default='')
    sent_timestamp = models.DateTimeField(
        null=True, blank=True, verbose_name='sent timestamp')
    pending = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     verbose_name='msg not received by', default=None)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='message',
        verbose_name='group key', blank=True, null=True)


# Room model for a conversation between random connected people
class Room(models.Model):  # room model
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          verbose_name='room participants', default=None, max_length=2)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(default=datetime.now() + timedelta(days=1))
    response = models.StringField(default="", max_length=2)

    def __str__(self):
        try:
            part1, part2 = self.participants.all()[0], self.participants.all()[1]
            return "{}-{}".format(part1.ph_num, part2.ph_num)
        except:
            return "null"

    class Meta:
        ordering = ('active', '-created',)

# Message model for each message inside a Dialogue
class RoomMessage(models.Model):    # message model
    msg_from = models.CharField(
        max_length=10, verbose_name='Message From', blank=True, null=True)
    msg_to = models.CharField(
        max_length=10, verbose_name='Message To', blank=True, null=True)
    message = models.CharField(max_length=1200)
    command = models.CharField(max_length=20, default='')
    sent_timestamp = models.DateTimeField(
        null=True, blank=True, verbose_name='sent timestamp')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='message',
        verbose_name='room key', default=None)

    def __str__(self):
        return self.msg_from

    class Meta:
        ordering = ('msg_to', 'msg_to', '-sent_timestamp',)
