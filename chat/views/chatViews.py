# imports
from ..serializers import DialogueSerializer, GroupSerializer, RoomSerializer
import json
from datetime import datetime as dt
from ..models import Group, Message, Dialogue, ActiveDetail, Room
from profileDetails.models import Ledger
from django.contrib.auth import get_user_model as User
from django.shortcuts import get_list_or_404, get_object_or_404
# rest framework imports
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from django.http import JsonResponse
# channels import
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.


class GenericPersonalViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    # serializer_class = UserSerializer
    # queryset = User.objects.all()

    def list(self, req, *args, **kwargs):
        pass

    # create a new personal chat
    def create(self, req, *args, **kwargs):

        # getting the http data
        data = req.data

        # creating return matrix and error handling sender and receiver
        info = {}
        msg_from = get_object_or_404(User(), ph_num=data['msg_from'])
        msg_to = get_object_or_404(User(), ph_num=data['msg_to'])

        # generate 2 dailogue to send messages
        info["msg_from"], from_created = Dialogue.objects.get_or_create(
            sender=msg_from, receiver=msg_to,)

        info["msg_to"], to_created = Dialogue.objects.get_or_create(
            sender=msg_to, receiver=msg_from,)

        # updating return info
        info["msg_from"] = info["msg_from"].sender.ph_num
        info["msg_to"] = info["msg_to"].sender.ph_num

        # printing the created outputs
        print(from_created, to_created)

        # editing our return data
        if from_created and to_created:
            info['info'] = 'created'

            # sending update to the receving user
            layer = get_channel_layer()

            async_to_sync(layer.group_send)(
                info["msg_to"],
                {
                    "message": {"type": "personal", "command": "create"},
                    "type": "update",
                    "msg_from": info["msg_from"],
                    "msg_to": info["msg_to"],
                    "sent_timestamp": dt.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                }
            )

        else:
            info['info'] = 'returned'

        # entering return code
        stat = status.HTTP_302_FOUND
        
        # giving back json response
        return JsonResponse(info, safe=False, status=stat)

    def update(self, req, *args, **kwargs):
        pass

    def retrieve(self, req, *args, **kwargs):
        pass

    # delete existing dialogue between 2 people 
    def delete(self, req, *args, **kwargs):

        # getting back the http data
        data = req.data

        # creating return matrix and error handling sender and receiver
        info = {}
        msg_from = get_object_or_404(User(), ph_num=data['msg_from'])
        msg_to = get_object_or_404(User(), ph_num=data['msg_to'])
        sender_dialogue = get_object_or_404(Dialogue, sender=msg_from, receiver=msg_to)
        receiver_dialogue = get_object_or_404(Dialogue, sender=msg_to, receiver=msg_from)

        # generate a dailogue to send message
        info["msg_from"] = sender_dialogue.delete()
        info["msg_to"] = receiver_dialogue.delete()

        # editing our return data
        info['info'] = "deleted"
        info['message'] = "Chat Deleted"

        # Sending update to the receving user
        layer = get_channel_layer()

        async_to_sync(layer.group_send)(
            data["msg_to"],
            {
                "message": {"type": "personal", "command": "delete"},
                "type": "update",
                "msg_from": data["msg_from"],
                "msg_to": data["msg_to"],
                "sent_timestamp": dt.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            }
        )

        # entering return code
        stat = status.HTTP_202_ACCEPTED 

        # giving back json response
        return JsonResponse(info, safe=False, status=stat)

class GenericGroupViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    def list(self, req, *args, **kwargs):
        pass

    def create(self, req, *args, **kwargs):

        data = req.data

        info = {}

        # saving serilizer data
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializerData = serializer.save()

            info = serializerData
            info['info'] = "created"
            stat = status.HTTP_201_CREATED

            # sending 'created' notification            
            if self.broadcast(serializerData['key'], serializerData['participants'], "create", data['admin'][0]):
                pass
            else:
                print("Error occured in sending notification in `create` of 'GenericGroupViewSet'")

            
        else:
            print("serializer error occured in 'GenericGroupViewSet'")
            print(serializer.errors)

            info['message'] = serializer.errors
            info['debug'] = "serializer error occured in 'GenericGroupViewSet'"
            info['info'] = "error"

            stat = status.HTTP_400_BAD_REQUEST

        return JsonResponse(info, safe=False, status=stat)

    def update(self, req, *args, **kwargs):
        data = req.data
        info = {}

        if data['command'] == 'leave':
            grp = get_object_or_404(Group, key=data['key'])
            msg_from = get_object_or_404(User(), ph_num=data['msg_from'])

            admin_length = grp.admin.all().count()
            participants_length = grp.participants.all().count()

            admin = True if msg_from in grp.admin.all() else False
            participant = True if msg_from in grp.participants.all() else False

            # sending 'leave' notification
            notifData = GroupSerializer(grp).data
            if self.broadcast(notifData['key'], notifData['participants'], data['command'], data['msg_from']):
                pass
            else:
                print("Error occured in sending notification in `update` of 'GenericGroupViewSet'")

            if admin_length == 1 and participants_length == 1 and admin and participant:
                grp.delete()

            else:
                if participant:
                    grp.participants.remove(msg_from)

                if admin:
                    grp.admin.remove(msg_from)
                    grp.admin.add(grp.participants.all()[0])

            info['info'] = "left"
            info['message'] = "the user has left the group"
            stat = status.HTTP_200_OK

        else :
            grp = get_object_or_404(Group, key=data['key'])
            msg_from = get_object_or_404(User(), ph_num=data['msg_from'])
            msg_to = get_object_or_404(User(), ph_num=data['msg_to'])

            if msg_from not in grp.admin.all():
                info['info'] = "error"
                info['message'] = "The Sender is not an Admin"
                stat = status.HTTP_400_BAD_REQUEST
            
            else:

                participant = True if (msg_to in grp.participants.all()) else False

                if data['command'] == 'add' and not participant:
                    if grp.participants.count() >= 128:
                        info['info'] = "error"
                        info['message'] = "Group Full"
                        stat = status.HTTP_501_NOT_IMPLEMENTED

                    else:
                        # adding receiver to the group
                        grp.participants.add(msg_to)

                        info['info'] = "added"
                        info['message'] = "The user has been added sucessfully"
                        stat = status.HTTP_200_OK

                elif data['command'] == 'remove' and participant:
                    # adding receiver to the group
                    grp.participants.remove(msg_to)

                    info['info'] = "removed"
                    info['message'] = "The user has been removed sucessfully"
                    stat = status.HTTP_200_OK

                elif data['command'] == 'promote' and participant:
                    grp.admin.add(msg_to)

                    info['info'] = "promoted"
                    info['message'] = "The user has been promoted sucessfully"
                    stat = status.HTTP_200_OK

                else:
                    info['info'] = "error"
                    info['message'] = "Wrong Operation"
                    stat = status.HTTP_501_NOT_IMPLEMENTED

                # sending notifications
                notifData = GroupSerializer(grp).data
                if self.broadcast(notifData['key'], notifData['participants'], data['command'], data['msg_from'], data['msg_to']):
                    pass
                else:
                    print("Error occured in sending notification in `create` of 'GenericGroupViewSet'")

        return JsonResponse(info, safe=False, status=stat)

    def retrieve(self, req, *args, **kwargs):
        pass

    def delete(self, req, *args, **kwargs):
        pass

    # sending notification to multiple people
    def broadcast(self, key, participants, command, msg_from=None, msg_to=None):

        # error handling the required data
        if not participants or key is None or command is None:
            True
        else:
            False
        
        # looping through all the prople in the group
        for ph_num in participants:
            
            # getting the layer object
            layer = get_channel_layer()

            # sending update to the receving user
            async_to_sync(layer.group_send)(
                ph_num,
                {
                    "message": {"type": "group", "command": command, "msg_from": msg_from, "msg_to": msg_to},
                    # "message": '{"type": "group", "command": "{}", "msg_from": "{}", "msg_to": "{}"}'.format(command, msg_from, msg_to),
                    "type": "update",
                    "msg_from": key,
                    "msg_to": ph_num,
                    "sent_timestamp": dt.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                }
            )

        return True

class GenericRoomViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    serializer_class = RoomSerializer
    queryset = User().objects.all()

    def list(self, req, *args, **kwargs):
        pass

    # create a new personal chat
    def create(self, req, *args, **kwargs):

        # getting the http data
        data = req.data

        # creating return matrix and error handling sender and receiver
        msg_from = get_object_or_404(User(), ph_num=data.pop('msg_from'))
        msg_to = get_object_or_404(User(), ph_num=data.pop('msg_to'))
        
        # removing entrys from Ledger
        try:
            Ledger.objects.filter(account=msg_from)[0].delete()
            Ledger.objects.filter(account=msg_to)[0].delete()
        except:
            print("error occured in deleting ledger in 'create' of 'GenericRoomViewSet'")

        data["participants"] = [msg_from.ph_num, msg_to.ph_num]

        # saving serilizer data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            print("111")
            instance = serializer.save()
            if instance['code'] == 400:
                return JsonResponse(instance, 
                safe=False, status=instance.pop("code"))

            # getting the data saved by the serializer
            serializerData = instance["data"]

            # sending 'create' notification
            notifData = serializerData
            if self.broadcast(notifData['participants'], command='create', msg_from=msg_from.ph_num, msg_to=msg_to.ph_num):
                pass
            else:
                print("Error occured in sending notification in `update` of 'GenericRoomViewSet'")

            # entering return code
            stat = status.HTTP_302_FOUND
        else:
            print("serializer error occured in 'create of room viewset'")
            print(serializer.errors)

            # entering return code
            stat = status.HTTP_400_BAD_REQUEST
        
        # giving back json response
        return JsonResponse(serializerData, safe=False, status=stat)

    # deactivate the room
    def update(self, req, *args, **kwargs):
        # getting back the http data
        data = req.data

        # creating return matrix and error handling sender
        info = {}
        msg_from = get_object_or_404(User(), ph_num=data['msg_from'])

        # leaving room if present in one
        rooms = get_list_or_404(Room, active=True,
                        participants=msg_from)

        # editing our return data
        info['info'] = "deactivated"
        info['message'] = "No Room is active anymore"

        # disabling all rooms if order is to match
        if len(rooms) > 0:
            for room in rooms:
                room.active = False
                room.save()

            # sending 'deactive' notification
            notifData = RoomSerializer(rooms[0]).data
            if self.broadcast(notifData['participants'], command='deactive', msg_from=data['msg_from']):
                pass
            else:
                print("Error occured in sending notification in `update` of 'GenericRoomViewSet'")


        # entering return code
        stat = status.HTTP_200_OK

        # giving back json response
        return JsonResponse(info, safe=False, status=stat)
    
    def retrieve(self, req, *args, **kwargs):
        pass

    # delete existing room between 2 people
    # TODO : (creating personal chats/updating score on the basis of matching)
    def delete(self, req, *args, **kwargs):
        # getting back the http data
        data = req.data

        # creating return matrix and error handling sender
        info = {}
        msg_from = get_object_or_404(User(), ph_num=data['msg_from'])

        # leaving room if present in one
        rooms = get_list_or_404(Room, active=True,
                        participants=msg_from)

        # deleting room
        if len(rooms) > 0:
            # sending 'deactive' notification
            notifData = RoomSerializer(rooms[0]).data
            if self.broadcast(notifData['participants'], command='delete', msg_from=data['msg_from']):
                pass
            else:
                print("Error occured in sending notification in `update` of 'GenericRoomViewSet'")

            rooms[0].delete()


        # editing our return data
        info['info'] = "deleted"
        info['message'] = "Room Deleted"

        # entering return code
        stat = status.HTTP_200_OK

        # giving back json response
        return JsonResponse(info, safe=False, status=stat)

    # sending notification to multiple people
    def broadcast(self, participants, command, msg_from=None, msg_to=None):

        # error handling the required data
        if not participants or command is None:
            True
        else:
            False
        
        # looping through all the prople in the group
        for ph_num in participants:
            
            # getting the layer object
            layer = get_channel_layer()

            # sending update to the receving user
            async_to_sync(layer.group_send)(
                ph_num,
                {
                    "message": {"type": "room", "command": command, "msg_from": msg_from, "msg_to": msg_to},
                    "type": "update",
                    "msg_from": msg_from,
                    "msg_to": ph_num,
                    "sent_timestamp": dt.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                }
            )

        return True

class GenericSpecialViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    def list(self, req, *args, **kwargs):
        pass

    # return all information
    def create(self, req, *args, **kwargs):

        # getting the http data
        data = req.data

        # create return dictionaly
        info = {}

        # creating return matrix and error handling sender and receiver
        msg_from = get_object_or_404(User(), ph_num=data.pop('msg_from'))

        try:
            # getting RAW data
            personal_chats = Dialogue.objects.filter(sender=msg_from)
            group_chats = Group.objects.filter(participants=msg_from)
            room_chats = Room.objects.filter(participants=msg_from, active=True)
            
            # serializing the data in loops
            convert = lambda book, func, obj : book.append(func(obj).data)

            # initializing objects and getting data
            if room_chats.exists(): 
                personals = []
                for j in range(len(personal_chats)): 
                    i = personal_chats[j]
                    convert(personals, DialogueSerializer, i)
                    personals[j]["sender"] = i.sender.ph_num
                    personals[j]["receiver"] = i.receiver.ph_num
            else : personals = []

            if room_chats.exists(): 
                groups = []
                for i in group_chats: convert(groups, GroupSerializer, i)
            else : groups = []

            if room_chats.exists() : rooms = RoomSerializer(room_chats[0]).data
            else : rooms = []        

            # putting the data in the return dict
            info["data"] = {}
            info["data"]["personal"] = personals
            info["data"]["group"] = groups
            info["data"]["room"] = rooms

            # add to info dictionary
            info["info"] = "success"
            info["message"] = "the data has been returned"

            # entering return code
            stat = status.HTTP_302_FOUND    

        except:
            print("serializer error occured in 'create of special viewset'")

            # add to info dictionary
            info['message'] = "some error occured at endpoint"
            info['info'] = "error"

            # entering return code
            stat = status.HTTP_400_BAD_REQUEST
        
        # giving back json response
        return JsonResponse(info, safe=False, status=stat)
    
    def update(self, req, *args, **kwargs):
        pass

    def retrieve(self, req, *args, **kwargs):
        pass

    def delete(self, req, *args, **kwargs):
        pass
                 
