# imports
import json
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Message, Dialogue, ActiveDetail
from django.conf import settings
from .serializers import MessageSerializer
# rest framework
from .serializers import MessageSerializer
# channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

Account = settings.AUTH_USER_MODEL

# command dictionary
commands = {
    # message based
    'new_msg',
    'msg_sent',
    'new_user',
    'new_grp_msg',
    'new_room_msg'
    'img',
    # time based
    'msg_received',
    'msg_read',
    'is_typing',
    'last_active',
    # special cases (for single user)
    'fetch_msgs',
    'delete_msgs',
    'delete_msg',
}

# initializing user model for querying
Account = get_user_model()


##################################################
######## Consumer for Personal Chats #############
##################################################


class ChatPersonalConsumer(WebsocketConsumer):
    def connect(self):
        # getting aguements (the phone numbers in string format)
        msg_to = self.scope['url_route']['kwargs']['msg_to']

        # setting the group name to the phone number of the receiver
        self.room_group_name = msg_to

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

    # Receive message from WebSocket and send them to group
    def receive(self, text_data):
        print("1")
        text_data_json = json.loads(text_data)

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
        print("2")

        # quering Account table and creating variables
        sender_pk = Account.objects.filter(ph_num=event['msg_from'])[0]
        receiver_pk = Account.objects.filter(ph_num=event['msg_to'])[0]
        msg_from = event['msg_from']
        sent_timestamp = event['sent_timestamp'],

        # editing serializer input data
        serializerData = event
        serializerData['command'] = 'msg_sent'
        serializerData['dialogue'] = Dialogue.objects.filter(
            sender=sender_pk, receiver=receiver_pk)[0].pk
        print(sent_timestamp)
        serializerData['sent_timestamp'] = sent_timestamp[0]

        # print(serializerData)

        # saving serilizer data
        serializer = MessageSerializer(data=serializerData)
        if serializer.is_valid():
            serializer.save()
        else:
            print("serializer error occured in 'new_msg'")
            print(serializer.errors)

        # editing serializer data for sending
        serializerData = serializer.validated_data
        # print(serializerData)

        serializerData['sent_timestamp'] = sent_timestamp
        serializerData.pop('dialogue')

        # sending data back to sender
        self.send(text_data=json.dumps(serializerData))

    def msg_received(self, event):
        # TODO : (save/update last_received_receiver)
        sender_pk = Account.objects.filter(ph_num=event['msg_from'])[0]
        receiver_pk = Account.objects.filter(ph_num=event['msg_to'])[0]
        sent_timestamp = event['sent_timestamp']

        # print(json.dumps(event, indent=2))

        # striping datetime from 'sent_timestamp'
        d = datetime.datetime.strptime(sent_timestamp, "%Y-%m-%d %H:%M:%S.%f")

        # querying the dialogue object that the data belongs to
        dialogue = Dialogue.objects.filter(
            sender=sender_pk, receiver=receiver_pk)

        # updating the value
        dialogue.update(last_received_receiver=d)

    def msg_read(self, event):
        # TODO : (save/update last_seen_receiver)
        sender_pk = Account.objects.filter(ph_num=event['msg_from'])[0]
        receiver_pk = Account.objects.filter(ph_num=event['msg_to'])[0]
        sent_timestamp = event['sent_timestamp']

        # print(json.dumps(event, indent=2))

        # striping datetime from 'sent_timestamp'
        d = datetime.datetime.strptime(sent_timestamp, "%Y-%m-%d %H:%M:%S.%f")

        # querying the dialogue object that the data belongs to
        dialogue = Dialogue.objects.filter(
            sender=sender_pk, receiver=receiver_pk)

        # updating the value
        dialogue.update(last_seen_receiver=d)

    def is_typing(self, event):
        # TODO : (send 'is_typing' messages)
        pass

    def last_active(self, event):
        # TODO : (getback details from Dailogue and ActiveDetails)

        command = event['type']
        msg_from = event['msg_from']
        msg_to = event['msg_to']
        sent_timestamp = event['sent_timestamp']

        # print(json.dumps(event, indent=2))

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'msg_from': msg_from,
            'msg_to': msg_to,
            'command': command,
            'sent_timestamp': sent_timestamp,
        }))


##################################################
######## Consumer for Group Chats ################
##################################################


class ChatGroupConsumer(WebsocketConsumer):
    pass

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

##################################################
######## Consumer for Special Commands ###########
##################################################


class ChatSpecialConsumer(WebsocketConsumer):

    def connect(self):
        # getting aguements
        user_num = self.scope['url_route']['kwargs']['user_num']
        # print(user_num)

        # self.channel_name = msg_from
        self.room_group_name = user_num

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

    # Receive message from WebSocket and send them to group
    def receive(self, text_data):
        print("3")
        text_data_json = json.loads(text_data)

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

    # Receive message from your group
    # [note : this will only work if the receiver is connected]
    def new_msg(self, event):
        print("4")

        # print(json.dumps(event, indent=2))

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'msg_from': event['msg_from'],
            'msg_to': event['msg_to'],
            'command': event['type'],
            'sent_timestamp': event['sent_timestamp'],
        }))

    # send response that the message was received by the receiver
    def msg_received(self, event):
        # TODO : (send last_received_receiver)

        command = event['type']
        msg_from = event['msg_from']
        msg_to = event['msg_to']
        sent_timestamp = event['sent_timestamp']

        # print(json.dumps(event, indent=2))

        # # Send message to WebSocket
        self.send(text_data=json.dumps({
            'msg_from': msg_from,
            'msg_to': msg_to,
            'command': command,
            'sent_timestamp': sent_timestamp,
        }))

    # send response that the message was seen by the receiver
    def msg_read(self, event):
        # TODO : (save/update last_seen_receiver)

        command = event['type']
        msg_from = event['msg_from']
        msg_to = event['msg_to']
        sent_timestamp = event['sent_timestamp']

        # print(json.dumps(event, indent=2))

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'msg_from': msg_from,
            'msg_to': msg_to,
            'command': command,
            'sent_timestamp': sent_timestamp,
        }))

    def is_typing(self, event):
        command = event['type']
        msg_from = event['msg_from']

        # print(json.dumps(event, indent=2))

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'msg_from': msg_from,
            'command': command,
        }))

    def last_active(self, event):
        command = event['type']
        msg_from = event['msg_from']
        msg_to = event['msg_to']
        sent_timestamp = event['sent_timestamp']

        # print(json.dumps(event, indent=2))

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'msg_from': msg_from,
            'msg_to': msg_to,
            'command': command,
            'sent_timestamp': sent_timestamp,
        }))
