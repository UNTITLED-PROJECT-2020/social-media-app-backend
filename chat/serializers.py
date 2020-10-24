# imports
from .models import Message, Dialogue
from . import models
# rest framework imports
from rest_framework import serializers

# creating serializers for models to work with


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Message
        fields = ['id', 'msg_from', 'msg_to', 'message',
                  'command', 'sent_timestamp', 'dialogue']


class DialogueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dialogue
        fields = ['sender', 'receiver', 'last_received_receiver',
                  'last_seen_receiver', ]
