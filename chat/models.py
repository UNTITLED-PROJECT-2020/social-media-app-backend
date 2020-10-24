# imports
from django.db import models
from django.conf import settings
# rest framework imports
from rest_framework.authtoken.models import Token

# Create your models here.


class Dialogue(models.Model):  # dialogue model
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender', default=None)
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver', default=None)
    last_received_receiver = models.DateTimeField(null=True, blank=True)
    last_seen_receiver = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.sender.username

    class Meta:
        ordering = ('receiver', '-last_seen_receiver',
                    '-last_received_receiver',)


class Message(models.Model):    # message model
    # sender = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender', default=None)
    # receiver = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver', default=None)
    msg_from = models.CharField(
        max_length=10, verbose_name='Message From', blank=True, null=True)
    msg_to = models.CharField(
        max_length=10, verbose_name='Message To', blank=True, null=True)
    message = models.CharField(max_length=1200)
    command = models.CharField(max_length=20, default='receive_msg')
    sent_timestamp = models.DateTimeField(
        null=True, blank=True, verbose_name='sent timestamp')
    dialogue = models.ForeignKey(
        Dialogue, on_delete=models.CASCADE, related_name='message',
        verbose_name='dialogue key', blank=True, null=True)
    # received_timestamp = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.msg_from

    class Meta:
        ordering = ('msg_to', '-sent_timestamp',)


class ActiveDetail(models.Model):
    active = models.BooleanField(default=True)
    last_active = models.DateTimeField(null=True, blank=True)
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activeDetail', verbose_name='user account', default=None)
