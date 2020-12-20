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
from ..serializers import RoomMessageSerializer, RoomSerializer
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

        # TODO : (Send back information saying that user is not present and disconnect)
        # querying the sender account
        self.sender = Account.objects.get(ph_num=self.msg_from)

        # getting the active room
        self.room = Room.objects.filter(active=True,
                        participants=self.sender)

        # printing the information
        print("SENDER : ", self.sender, ", ROOM : ", self.room[0].active, self.room[0].participants.all())

        # TODO : (deactivate if time is beyond "finished" field in room)
        # TODO : (deactivate if user is not in a room)
        
        self.room = self.room[0]

            # getting receiver object
        self.receiver = self.room.participants.all().exclude(pk=self.sender.pk)[0]

    # disconnect from the current layer
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message and send them to type 
    def receive(self, text_data):
        # print("1")
        text_data_json = json.loads(text_data)

        # print(text_data_json)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'message': text_data_json['message'],
                'type': text_data_json['command'],
                'msg_from': text_data_json['msg_from'],
                'msg_to': text_data_json['msg_to'],
                'sent_timestamp': text_data_json['sent_timestamp'],
            }
        )

    # Receive message reply from the message you sent
    def new_msg(self, event):
        print("in the 'new_msg' of the room sender")

        # editing event data
        event['msg_to'] = self.receiver.ph_num
        event['command'] = event.pop('type')

        # saving serilizer data
        serializer = RoomMessageSerializer(data=event)
        if serializer.is_valid():
            serializer.save()

            # getting the data saved by the serializer
            serializerData = serializer.validated_data
        else:
            print("serializer error occured in 'new_msg'")
            print(serializer.errors)

        # editing serializer data for recever
        serializerData['sent_timestamp'] = event['sent_timestamp']

        # broadcasting the pending receiver
        self.broadcast(serializerData)

        # editing serializer data for sender
        serializerData['message'] = event['sent_timestamp']
        serializerData['sent_timestamp'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%Z')
        serializerData['command'] = 'msg_sent'
        print(serializerData)

        # sending data back to sender
        self.send(text_data=json.dumps(serializerData))

    # send received command on a previous message
    def msg_received(self, event):
        event["command"] = event.pop("type")

        # broadcasting the received message
        self.broadcast(event)

        # deleting the message
        self.delete_msg(event)

    # send read command on a previous message
    def msg_read(self, event):
        event["command"] = event.pop("type")

        # broadcasting the received message
        self.broadcast(event)

    # send information that the user is typing
    def is_typing(self, event):
        event["command"] = event.pop("type")

        # broadcasting the received message
        self.broadcast(event)

    # broadcasting an event to other people
    def broadcast(self, event):
        print("==In broadcast==")

        # adding type to our event
        event['type'] = event.pop('command')
        event['msg_from'] = "room"
        event['msg_to'] = self.receiver.ph_num

        # print(event)

        # sending message to all receivers in the group
        async_to_sync(self.channel_layer.group_send)(
            event['msg_to'],
            event
        )

    # fetch saved messages
    def fetch_msgs(self, event):
        pass

    # delete a message
    def delete_msg(self, event):

        # querying dataset
        d = datetime.datetime.strptime(event['message'], "%Y-%m-%dT%H:%M:%S.%f%z")
        room_msg = self.room.message.filter(msg_from=event['msg_to'], sent_timestamp=d)

        # error handling if queryset is empty
        if room_msg.exists():
            # deleting the queryset object
            room_msg[0].delete()

        else:
            # Send error message to WebSocket
            event['command'] = "delete_msg"
            event['message'] = "could not find the message you wanted to delete"

            self.error(event)
            pass

        pass

    # send an error reply
    def error(self, event):

        # sending back an error event
        self.send(text_data=json.dumps({
            'msg_from': event['msg_from'],
            'msg_to': event['msg_to'],
            'command': "error",
            'type': event['command'],
            'message': event['message'],
        }))