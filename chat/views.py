# imports
from django.shortcuts import render
import json
from django.utils.safestring import mark_safe
# rest framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework import viewsets

# Create your views here.


class GenericMessageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # return username if login with any other field (i.e. : phone number, email)

    def create(self, req):  # post method
        data = {}  # creating data dictionary to send as response
        if req.data:
            print("nothing yet")

        else:
            data["error"] = "no data provided"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


# testing urls

##################################################
######## views for Personal Chats #############
##################################################
def personalIndex(request):
    return render(request, 'personal/index.html', {})


def personalRoom(request, msg_from, msg_to):
    return render(request, 'personal/room.html', {
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

##################################################
######## views for Special Chats #############
##################################################

# TODO : (get ActiveDetail of a user)
# TODO : (get last_seen_receiver of a Dialogue)
