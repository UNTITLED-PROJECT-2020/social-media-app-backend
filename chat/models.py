# imports
from django.db import models
from django.conf import settings
# rest framework imports
from rest_framework.authtoken.models import Token

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender', default=None)
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver', default=None)
    message = models.CharField(max_length=1200)
    command = models.CharField(max_length=20, default='receive_msg')
    sent_timestamp = models.DateTimeField(
        null=True, blank=True)
    # received_timestamp = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.sender.username

    class Meta:
        ordering = ('receiver', '-sent_timestamp',)
