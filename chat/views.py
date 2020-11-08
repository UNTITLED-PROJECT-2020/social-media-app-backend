# imports
import json
from django.utils.safestring import mark_safe
from .models import Message, Dialogue, ActiveDetail
from django.contrib.auth import get_user_model as User
from django.shortcuts import get_list_or_404, get_object_or_404, render
# rest framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse

# Create your views here.

'''
endpoints to br implemented :

    - get/update last_active (or check if user is active right now)
    - get/update last_received_receiver
    - get/update last_seen_receiver
    - new_user (dialogue)
    - new_grp
    - new_room
'''


class GenericInfoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    # retrieve different types of chat information, render index and update time information
    # serializer_class = ActiveDetail
    # queryset = ActiveDetail.objects.all()

    def list(self, req, *args, **kwargs):
        # render index page
        return render(req, 'info/index.html', {})

    def retrieve(self, req, *args, **kwargs):

        try:
            user_num = self.kwargs['user_num']
        except:
            user_num = None

        try:
            msg_from = self.kwargs['msg_from']
            msg_to = self.kwargs['msg_to']
        except:
            msg_from = None
            msg_to = None

        print(user_num == None, msg_from, msg_to)
        if user_num is None:
            print("mahshallah")
        # configuring which type of request is sent

        if (msg_from == None and msg_to == None):
            # get active details
            try:
                data = get_object_or_404(User(), ph_num=user_num).activeDetail
                info = {}
                info["active"] = data.active
                info["last_active"] = data.last_active
            except:
                err = {
                    "err": "Active Details Not Found",
                }
                # data = User().objects.get(ph_num=user_num).activeDetail
                return JsonResponse(err, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({"data": info}, safe=False, status=status.HTTP_302_FOUND)
        elif user_num is None:
            # get seen/receive details
            data = get_object_or_404(
                Dialogue,
                sender=User().objects.get(ph_num=msg_from),
                receiver=User().objects.get(ph_num=msg_to))
            info = {}
            info["last_received_receiver"] = data.last_received_receiver
            info["last_seen_receiver"] = data.last_seen_receiver
            return JsonResponse(info, safe=False, status=status.HTTP_302_FOUND)

        else:
            err = {
                "err": "incorrect url",
            }
            return JsonResponse(err, status=status.HTTP_404_NOT_FOUND)

    def update(self, req, *args, **kwargs):

        user_num = self.kwargs['user_num']
        data = req.data

        if (data['command'] == 'activate'):
            info = get_object_or_404(User(), ph_num=user_num).activeDetail

            info.active = True
            info.last_active = data['last_active']
            info.save()

            return JsonResponse({"Response": "Data Updated"}, safe=False, status=status.HTTP_200_OK)

        elif (data['command'] == 'deactivate'):
            info = get_object_or_404(User(), ph_num=user_num).activeDetail

            info.active = False
            info.last_active = data['last_active']
            info.save()

            return JsonResponse({"Response": "Data Updated"}, safe=False, status=status.HTTP_200_OK)

        else:
            err = {
                "err": "incorrect request/url",
            }
            return JsonResponse(err, status=status.HTTP_404_NOT_FOUND)


class GenericSpecialViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    def list(self, req, *args, **kwargs):
        # render index page
        return render(req, 'special/index.html', {})

    def create(self, req, *args, **kwargs):

        generate = self.kwargs['generate']
        data = req.data

        # configuring which type of request is sent

        if (generate == "personal"):
            # create personal dialogue

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

        elif (generate == "group"):     # create group dialogue
            # get active details
            # TODO : (Create Group Chat)
            data = Dialogue.objects.get(sender=msg_from, receiver=msg_to)
            return JsonResponse(data, safe=False)
        elif (generate == "room"):  # create room dialogue
            # get active details
            # TODO : (Create Room Chat)
            data = Dialogue.objects.get(sender=msg_from, receiver=msg_to)
            return JsonResponse(data, safe=False)
        else:   # Send 404 error
            err = {
                "err": "incorrect url",
            }
            return JsonResponse(err, status=status.HTTP_404_NOT_FOUND)

# testing urls

##################################################
######## views for Personal Chats #############
##################################################
# wss//:


def personalIndex(request):
    return render(request, 'personal/index.html', {})


def personalRoom(request, msg_from, msg_to):
    return render(request, 'personal/room.html', {
        'msg_from': msg_from,
        'msg_to': msg_to,
    })


def personalIndexTest(request):
    return render(request, 'personal/testing/index.html', {})


def personalRoomTest(request, msg_from, msg_to):
    return render(request, 'personal/testing/room.html', {
        'msg_from': msg_from,
        'msg_to': msg_to,
    })

##################################################
######## views for Group Chats #############
##################################################

##################################################
######## views for ChatRoom Chats #############
##################################################


def chatRoomIndex(request):
    return render(request, 'room/index.html', {})


def chatRoom(request, room_name):
    return render(request, 'room/room.html', {
        'room_name': room_name
    })

# test

##################################################
######## views for Special Chats #############
##################################################
