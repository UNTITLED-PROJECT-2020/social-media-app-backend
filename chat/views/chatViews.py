# imports
from chat.serializers import GroupSerializer
import json
import datetime
from ..models import Group, Message, Dialogue, ActiveDetail
from django.contrib.auth import get_user_model as User
from django.shortcuts import get_object_or_404
# rest framework imports
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from django.http import JsonResponse

# Create your views here.


class GenericPersonalViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    # serializer_class = UserSerializer
    # queryset = User.objects.all()

    def list(self, req, *args, **kwargs):
        pass

    def create(self, req, *args, **kwargs):

        data = req.data

        info = {}
        msg_from = get_object_or_404(User(), ph_num=data['msg_from'])
        msg_to = get_object_or_404(User(), ph_num=data['msg_to'])

        # generate a dailogue to send message
        info["msg_from"], from_created = Dialogue.objects.get_or_create(
            sender=msg_from, receiver=msg_to,)

        info["msg_to"], to_created = Dialogue.objects.get_or_create(
            sender=msg_to, receiver=msg_from,)

        print(from_created, to_created)

        if from_created and to_created:
            info['info'] = 'created'
        else:
            info['info'] = 'returned'

        info["msg_from"] = info["msg_from"].sender.ph_num
        info["msg_to"] = info["msg_to"].sender.ph_num

        stat = status.HTTP_302_FOUND

        return JsonResponse(info, safe=False, status=stat)

    def update(self, req, *args, **kwargs):
        pass

    def retrieve(self, req, *args, **kwargs):
        pass

    def delete(self, req, *args, **kwargs):

        data = req.data

        info = {}
        msg_from = get_object_or_404(User(), ph_num=data['msg_from'])
        msg_to = get_object_or_404(User(), ph_num=data['msg_to'])

        # generate a dailogue to send message
        info["msg_from"] = Dialogue.objects.get(
            sender=msg_from, receiver=msg_to).delete()
        info["msg_to"] = Dialogue.objects.get(
            sender=msg_to, receiver=msg_from).delete()

        
        info['info'] = "deleted"
        info['message'] = "Chat Deleted"

        stat = status.HTTP_202_ACCEPTED 

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

            if admin_length == 1 and participants_length == 1 and admin and participant:
                grp.delete()
                # Group.objects.delete()

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

        return JsonResponse(info, safe=False, status=stat)

    def retrieve(self, req, *args, **kwargs):
        pass

    def delete(self, req, *args, **kwargs):
        pass
class GenericRoomViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    def create(self, req, *args, **kwargs):

        data = req.data

        # # get active details
        # # TODO : (Create Room Chat)
        # # data = Dialogue.objects.get(sender=msg_from, receiver=msg_to)
        # return JsonResponse(data, safe=False)
    

class GenericSpecialViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    def create(self, req, *args, **kwargs):

        data = req.data

        info = {}
        msg_from = get_object_or_404(User(), ph_num=data['msg_from'])
        msg_to = get_object_or_404(User(), ph_num=data['msg_to'])

        # generate a dailogue to send message
        info["msg_from"], from_created = Dialogue.objects.get_or_create(
            sender=msg_from, receiver=msg_to)
        info["msg_to"], to_created = Dialogue.objects.get_or_create(
            sender=msg_to, receiver=msg_from)

        if from_created and to_created:
            info['info'] = 'created'
        else:
            info['info'] = 'returned'

        info["msg_from"] = info["msg_from"].sender.ph_num
        info["msg_to"] = info["msg_to"].sender.ph_num

        # info["msg_from"]
        print(info)

        return JsonResponse(info, safe=False)
