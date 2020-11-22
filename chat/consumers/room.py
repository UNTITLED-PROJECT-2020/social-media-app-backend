# imports
import json
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from ..models import Message, Dialogue, ActiveDetail
from django.conf import settings
from ..serializers import MessageSerializer
# rest framework
from rest_framework.renderers import JSONRenderer
from ..serializers import MessageSerializer, GroupMessageSerializer
# channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

Account = settings.AUTH_USER_MODEL

'''
# commands (for single user)

    # message based

    [*]  'new_msg',
    []  'new_room_msg'
    []  'img',

    # time based

    [*]  'msg_sent',
    [*]  'msg_received',
    [*]  'msg_read',
    [*]  'is_typing',

    # special cases 

    [*]  'fetch_msgs',
    [*]  'delete_msgs',
    [*]  'delete_msg',

    # error handling

    [*] 'error',
}
'''

'''
# commands (for groups user)

    # message based

    []  'new_grp_msg',

    # time based

    []  'msg_sent',
    []  'msg_received',
    []  'msg_read',
    []  'is_typing',

    # special cases

    [*]  'fetch_msgs',
    [*]  'delete_msgs',

    # error handling

    [*] 'error',
}
'''

# initializing user model for querying
Account = get_user_model()

##################################################
######## Consumer for Chat-room Chats ############
##################################################


class ChatRoomConsumer(WebsocketConsumer):
    # helper functions
    def fetch_messages(self, data):
        pass

    def new_message(self, data):
        pass

    # main functions
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
