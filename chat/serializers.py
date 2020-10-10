# imports
from .models import Message
from . import models
# rest framework imports
from rest_framework import serializers

# creating serializers for models to work with


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Message
        fields = ['sender', 'receiver', 'message', 'command', 'sent_timestamp']
