# imports
import json
import datetime
from django.contrib.auth import get_user_model
from ..models import Message, Dialogue
from ..serializers import MessageSerializer
# rest framework
from ..serializers import MessageSerializer
# channels
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# initializing user model for querying
Account = get_user_model()

# TODO : Check if users are in a dialogue
# TODO : (Add Error handling using the error method)


##################################################
######## Consumer for Personal Chats #############
##################################################


class ChatPersonalConsumer(WebsocketConsumer):
    # connect to the layer
    def connect(self):
        # getting aguements (the phone numbers in string format)
        msg_to = self.scope['url_route']['kwargs']['msg_to']
        msg_from = self.scope['url_route']['kwargs']['msg_from']

        # setting the group name to the phone number of the receiver
        self.room_group_name = msg_to

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    # disconnect from the current layer
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket and send them to group
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

        # quering Account table and creating variables
        sender_pk = Account.objects.filter(ph_num=event['msg_from'])[0]
        receiver_pk = Account.objects.filter(ph_num=event['msg_to'])[0]
        msg_from = event['msg_from']

        sent_timestamp = event['sent_timestamp'],

        # editing serializer input data
        serializerData = event
        serializerData['dialogue'] = Dialogue.objects.get(
            sender=sender_pk, receiver=receiver_pk).pk

        serializerData['command'] = event.pop('type')

        # saving serilizer data
        serializer = MessageSerializer(data=serializerData)
        if serializer.is_valid():
            serializer.save()
        else:
            print("serializer error occured in 'new_msg'")
            print(serializer.errors)

        # editing serializer data for sending
        serializerData = serializer.validated_data

        # adding current time to sent_timestamp
        serializerData['sent_timestamp'] = datetime.datetime.now().strftime(
            '%Y-%m-%dT%H:%M:%S.%f%Z')
        serializerData['command'] = 'msg_sent'
        serializerData['message'] = sent_timestamp[0]
        serializerData.pop('dialogue')

        # sending data back to sender
        self.send(text_data=json.dumps(serializerData))

    # send received command on a previous message
    def msg_received(self, event):
        # save/update last_received_receiver
        sender_pk = Account.objects.filter(ph_num=event['msg_from'])[0]
        receiver_pk = Account.objects.filter(ph_num=event['msg_to'])[0]
        sent_timestamp = event['sent_timestamp']

        # striping datetime from 'sent_timestamp'
        d = datetime.datetime.strptime(sent_timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")

        # querying the dialogue object that the data belongs to
        dialogue = Dialogue.objects.filter(
            sender=sender_pk, receiver=receiver_pk)

        # updating the value
        dialogue.update(last_received_receiver=d)

        # automatically deleting message
        self.delete_msg(event)

    # send read command on a previous message
    def msg_read(self, event):
        # save/update last_seen_receiver
        sender_pk = Account.objects.filter(ph_num=event['msg_from'])[0]
        receiver_pk = Account.objects.filter(ph_num=event['msg_to'])[0]
        sent_timestamp = event['sent_timestamp']

        # print(json.dumps(event, indent=2))

        # striping datetime from 'sent_timestamp'
        d = datetime.datetime.strptime(sent_timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")

        # querying the dialogue object that the data belongs to
        dialogue = Dialogue.objects.filter(
            sender=sender_pk, receiver=receiver_pk)

        # updating the value
        dialogue.update(last_seen_receiver=d)

    # send information that the user is typing
    def is_typing(self, event):
        pass

    # fetch saved messages
    def fetch_msgs(self, event):
        pass

    # delete a message
    def delete_msg(self, event):

        # querying dataset
        msg = Message.objects.filter(
            msg_from=event['msg_to'],
            msg_to=event['msg_from'],
            sent_timestamp=event['message'])

        # error handling if queryset is empty
        if msg.exists():
            # deleting the queryset object
            msg[0].delete()

        else:
            # Send error message to WebSocket
            event['command'] = "delete_msg"
            event['message'] = "could not find the message you wanted to delete"

            self.error(event)
            pass

        pass

    # send updates to user
    def update(self, event):
        print("in update of 'personal'")
        
        # TODO : (save update message) 
                
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
