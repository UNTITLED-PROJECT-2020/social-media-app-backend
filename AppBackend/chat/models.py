# imports
from django.db import models
from django.conf import settings
from django.conf.settings import AUTH_USER_MODEL as User
# rest framework imports
from rest_framework.authtoken.models import Token

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanFeild(default=False)

    def __str__(self):
         return self.message

     class Meta:
         ordering = ('timestamp',)
