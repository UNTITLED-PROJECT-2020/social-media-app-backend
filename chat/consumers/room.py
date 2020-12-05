# imports
import json
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from ..models import Room, RoomMessage
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

# TODO : Check if users are in a group
# TODO : (Add Error handling using the error method)

# initializing user model for querying
Account = get_user_model()

##################################################
######## Consumer for Chat-room Chats ############
##################################################


class ChatRoomConsumer(WebsocketConsumer):
    # connect to the layer
    def connect(self):
        self.msg_from = self.scope['url_route']['kwargs']['msg_from']
        self.room_group_name = 'room_%s' % self.msg_from

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.sender = Account.objects.get(ph_num=self.msg_from)

        self.room = Room.objects.filter(active=True,
                        participants=self.sender)

        print("SENDER : ", self.sender, ", ROOM : ", self.room[0].active, self.room[0].participants.all())

        if len(self.room) > 1:

            # TODO : (Send Back Message and deactivate all)
            # error
            pass
        else:
            self.room = self.room[0]

    # disconnect from the current layer
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message and send them to type 
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

    # Receive message reply from the message you sent
    def new_msg(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    # send received command on a previous message
    def msg_recived(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    # send read command on a previous message
    def msg_seen(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    # send information that the user is typing
    def is_typing(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    # fetch saved messages
    def fetch_msgs(self, event):
        pass

    # delete a message
    def delete_msg(self, event):

        # querying dataset
        # msg = Message.objects.filter(
        #     msg_from=event['msg_to'],
        #     msg_to=event['msg_from'],
        #     sent_timestamp=event['message'])

        # error handling if queryset is empty
        # if msg.exists():
        #     # deleting the queryset object
        #     msg[0].delete()

        # else:
        #     # Send error message to WebSocket
        #     event['command'] = "delete_msg"
        #     event['message'] = "could not find the message you wanted to delete"

        #     self.error(event)
        #     pass

        pass

    # send an error reply
    def error(self, event):
        self.send(text_data=json.dumps({
            'msg_from': event['msg_from'],
            'msg_to': event['msg_to'],
            'command': "error",
            'type': event['command'],
            'message': event['message'],
        }))