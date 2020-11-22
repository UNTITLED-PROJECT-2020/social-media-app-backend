# imports
import json
import datetime
from django.contrib.auth import get_user_model
from ..models import Group, GroupMessage, Message
from django.conf import settings
# rest framework
from ..serializers import GroupMessageSerializer
# channels
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# initializing user model for querying
Account = get_user_model()

# TODO : Check if users are in a group
# TODO : (Add Error handling using the error method)

##################################################
######## Consumer for Group Chats ################
##################################################


class ChatGroupConsumer(WebsocketConsumer):
    # connect to the layer
    def connect(self):
        # getting aguements (the phone numbers in string format)
        grp_name = self.scope['url_route']['kwargs']['grp_name']
        msg_from = self.scope['url_route']['kwargs']['msg_from']

        # setting the group name to the phone number of the receiver
        self.room_group_name = grp_name + '-' + msg_from

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
        # print("In the group 'receive' of", self.room_group_name)

        if type(text_data) is type({}):
            text_data_json = text_data
        else:
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

    # Broadcast a new message
    def new_grp_msg(self, event):
        # print(event)
        # adding data
        serializerData = event

        # adding extra needed fields
        serializerData['pending'] = []
        serializerData['group'] = None

        # saving serilizer data
        serializer = GroupMessageSerializer(data=serializerData)
        if serializer.is_valid():
            serializerData = serializer.save()
        else:
            print("serializer error occured in 'new_msg'")
            print(serializer.errors)

        # broadcasting all over the pending
        self.broadcast(serializerData)

    # Receive message reply from the message you sent
    def new_msg(self, event):
        # print("In the group 'new_msg' of", self.room_group_name)

        # removing 'type' field
        event.pop('type')

        # adding command
        event['command'] = "msg_sent"

        # putting sent_timestamp to the message for identification
        event['message'] = event['sent_timestamp']

        # adding current time to sent_timestamp
        event['sent_timestamp'] = datetime.datetime.now().strftime(
            '%Y-%m-%dT%H:%M:%S.%f%Z')

        # print(event)

        # sending data back to sender
        self.send(text_data=json.dumps(event))

    # broadcast 'msg_received' reply from user
    def grp_msg_received(self, event):
        # print("In the group 'grp_msg_received' of", self.room_group_name)
        # print(event)

        try:
            grp = Group.objects.get(key=event['msg_to'])
            grp_message = grp.message.get(
                sent_timestamp=event['message'])
        except Group.DoesNotExist as e:
            print("exception in group 'grp_msg_received'")
            return
        except GroupMessage.DoesNotExist as e:
            print("exception in group 'grp_msg_received'")
            return

        # modifying event data
        event.pop('type')
        event['command'] = "msg_received"
        event['pending'] = []

        # adding pending field
        for person in grp.participants.all():
            if person.ph_num != event['msg_from']:
                event['pending'].append(person.ph_num)

        # broadcasting message to all pending users
        self.broadcast(event)

        # Group Message Updation
        if (grp_message.pending.count() <= 1):
            # delete message if last pending
            print("message deleted")
            grp_message.delete()
        else:
            # remove user from pending
            print("user removed from pending")
            grp_message.pending.remove(
                Account.objects.get(ph_num=event['msg_from']))

    # 'msg_received' reply from user when he gets a new message
    def msg_received(self, event):
        # print("In the group 'msg_received' of", self.room_group_name)
        pass

    # broadcast 'msg_read' reply from user
    def grp_msg_read(self, event):
        # print("In the group 'grp_msg_read' of", self.room_group_name)
        # print(event)

        try:
            grp = Group.objects.get(key=event['msg_to'])
        except Group.DoesNotExist as e:
            print("exception in group 'grp_msg_read'")
            return

        # modifying event data
        event.pop('type')
        event['command'] = "msg_read"
        event['pending'] = []

        # adding pending field
        for person in grp.participants.all():
            if person.ph_num != event['msg_from']:
                event['pending'].append(person.ph_num)

        # broadcasting message to all pending users
        self.broadcast(event)

    # 'msg_read' reply from user when he sees the new message
    def msg_read(self, event):
        # print("In the group 'msg_read' of", self.room_group_name)
        pass

    # broadcast is typing to the group
    def is_grp_typing(self, event):
        # print("In the group 'is_grp_typing' of", self.room_group_name)
        # print(event)

        try:
            grp = Group.objects.get(key=event['msg_to'])
        except Group.DoesNotExist as e:
            print("exception in group 'is_grp_typing'")
            return

        # modifying event data
        event.pop('type')
        event['command'] = "is_typing"
        event['pending'] = []

        # adding pending field
        for person in grp.participants.all():
            if person.ph_num != event['msg_from']:
                event['pending'].append(person.ph_num)

        # broadcasting message to all pending users
        self.broadcast(event)

    # send information that the user is typing
    def is_typing(self, event):
        # print("In the group 'is_typing' of", self.room_group_name)
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

            pass
        else:
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'msg_from': event['msg_from'],
                'msg_to': event['msg_to'],
                'command': "error",
                'type': 'delete_msg',
                'message': "could not find the message you wanted to delete",
            }))
            pass

        pass

    # broadcasting an event to other people
    def broadcast(self, event):
        # print("========in broadcast========")

        sendData = {
            'message': event['message'],
            'command': event['command'],
            'type': "receive",
            'msg_from': self.room_group_name,
            'msg_to': "",
            'sent_timestamp': event['sent_timestamp'],
        }

        # looping through all receivers
        for ph_num in event['pending']:

            # udating the 'msg_to' field
            sendData['msg_to'] = ph_num

            # sending message to all receivers in the group
            async_to_sync(self.channel_layer.group_send)(
                ph_num,
                sendData
            )

            # # I want to
            # break
            # # free

        # sending message to sender consumer for success message
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            sendData
        )

    # send an error reply
    def error(self, event):
        self.send(text_data=json.dumps({
            'msg_from': event['msg_from'],
            'msg_to': event['msg_to'],
            'command': "error",
            'type': event['command'],
            'message': event['message'],
        }))
