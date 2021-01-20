# imports
import json
from django.contrib.auth import get_user_model
from ..models import Message
from ..serializers import MessageSerializer, RoomMessageSerializer
# rest framework
from ..serializers import MessageSerializer, GroupMessageSerializer
# channels
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# initializing user model for querying
Account = get_user_model()

##################################################
######## Consumer for Special Commands ###########
##################################################

# TODO : Check if the receiver of a message
# is same as the user connected to this consumer
# TODO : (Add Error handling using the error method)


class ChatSpecialConsumer(WebsocketConsumer):

    def connect(self):
        # getting aguements
        user_num = self.scope['url_route']['kwargs']['user_num']

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
        # print("In the special 'receive' of", self.room_group_name)

        if type(text_data) is type({}):
            text_data_json = text_data
        else:
            text_data_json = json.loads(text_data)

        # TODO : Error Handling for wrong user receive
        if text_data_json['msg_to'] != self.room_group_name:
            return

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

    # Receive message from your group (if the receiver is connected)
    def new_msg(self, event):
        # print("In the special 'new_msg' of", self.room_group_name)
        # print(event)
        # print(self.user_num)

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
        # print("In the special 'msg_received' of", self.room_group_name)
        # print(event)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'msg_from': event['msg_from'],
            'msg_to': event['msg_to'],
            'command': event.pop('type'),
            'sent_timestamp': event['sent_timestamp'],
        }))

        pass

    # send response that the message was seen by the receiver
    def msg_read(self, event):
        # print("In the special 'msg_read' of", self.room_group_name)

        # print(event)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'msg_from': event['msg_from'],
            'msg_to': event['msg_to'],
            'command': event.pop('type'),
            'sent_timestamp': event['sent_timestamp'],
        }))

        pass

    # send response that the sender is typing to the receiver
    def is_typing(self, event):
        # print("In the special 'is_typing' of", self.room_group_name)

        # print(event)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'msg_from': event['msg_from'],
            'msg_to': event['msg_to'],
            'command': event.pop('type'),
            'sent_timestamp': event['sent_timestamp'],
        }))

        pass

    # fetch personal messages
    def fetch_msgs(self, event):
        # print(event)
        # getting aguements
        user_num = self.scope['url_route']['kwargs']['user_num']

        # querying dataset
        msgs = Message.objects.filter(
            # msg_from=event['msg_from'],
            msg_to=user_num,)

        # serializing the queryset objects
        serializer = MessageSerializer(msgs, many=True)

        serializerData = []

        # removing 'id' and 'dialogue' fields from each dictionary
        serializerData = [{k: v for k, v in d.items() if (
            k != 'id' and k != 'dialogue')} for d in serializer.data]

        # getting the length and iterations of the serializerData array
        length = len(serializerData)
        iters = round(length/10)

        # checking if the length of array is a multiple of 10
        if (len == iters*10):
            iters -= 1

        # looping over 10 messages and sending
        for i in range(iters):
            # data to be sent back
            data = {
                'command': "fetch_msgs",
                'messages': json.dumps(serializerData[(i*10): (i+1)*10]),
                'all': False
            }

            # Send message to WebSocket
            self.send(text_data=json.dumps(data))

        # last amount of data to be sent back
        data = {
            'command': "fetch_msgs",
            'messages': json.dumps(serializerData[-(length - iters*10):]),
            'all': True
        }

        # Send message to WebSocket
        self.send(text_data=json.dumps(data))

    # fetch group messages
    def fetch_grp_msgs(self, event):
        # print("In the special 'fetch_grp_msgs' of", self.room_group_name)
        # print(event)

        user = Account.objects.get(ph_num=event['msg_to'])
        grp_msgs = user.groupmessage_set.all()

        serializerData = []

        for grp_msg in grp_msgs:
            msg = GroupMessageSerializer(grp_msg).data

            # editing data
            msg.pop('group')
            msg['msg_from'] = msg['msg_to'] + '-' + msg['msg_from']
            msg['msg_to'] = self.room_group_name

            serializerData.append(msg)
        pass

        # sending back data in chunks

        # getting the length and iterations of the serializerData array
        length = len(serializerData)
        iters = round(length/10)

        # checking if the length of array is a multiple of 10
        if (len == iters*10):
            iters -= 1

        # looping over 10 messages and sending
        for i in range(iters):
            # data to be sent back
            data = {
                'command': "fetch_grp_msgs",
                'messages': json.dumps(serializerData[(i*10): (i+1)*10]),
                'all': False
            }

            # Send message to WebSocket
            self.send(text_data=json.dumps(data))

        # last amount of data to be sent back
        data = {
            'command': "fetch_grp_msgs",
            'messages': json.dumps(serializerData[-(length - iters*10):]),
            'all': True
        }

        # Send message to WebSocket
        self.send(text_data=json.dumps(data))

    # fetch room messages
    def fetch_room_msgs(self, event):
        # print("In the special 'fetch_grp_msgs' of", self.room_group_name)
        # print(event)

        user = Account.objects.get(ph_num=event['msg_to'])
        room_msgs = user.room_set.all()[0].message.filter(msg_to=event['msg_to'])

        serializerData = []

        for grp_msg in room_msgs:
            msg = RoomMessageSerializer(grp_msg).data

            # editing data
            msg.pop('room')
            msg['msg_from'] = "room"

            serializerData.append(msg)
        pass

        # # sending back data in chunks

        # getting the length and iterations of the serializerData array
        length = len(serializerData)
        iters = round(length/10)

        # checking if the length of array is a multiple of 10
        if (len == iters*10):
            iters -= 1

        # looping over 10 messages and sending
        for i in range(iters):
            # data to be sent back
            data = {
                'command': "fetch_room_msgs",
                'messages': json.dumps(serializerData[(i*10): (i+1)*10]),
                'all': False
            }

            # Send message to WebSocket
            self.send(text_data=json.dumps(data))

        # last amount of data to be sent back
        data = {
            'command': "fetch_room_msgs",
            'messages': json.dumps(serializerData[-(length - iters*10):]),
            'all': True
        }

        # Send message to WebSocket
        self.send(text_data=json.dumps(data))

    # delete a message
    def delete_msg(self, event):
        pass

    # send updates to user
    def update(self, event):
        print("in update of 'special'")
        event['command'] = event.pop('type')
        print(event)

        
        self.send(text_data=json.dumps(event))
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
