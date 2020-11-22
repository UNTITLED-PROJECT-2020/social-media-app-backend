# imports
from chat.serializers import GroupSerializer
import uuid
import json
from django.utils.safestring import mark_safe
from ..models import Group, Message, Dialogue, ActiveDetail
from django.contrib.auth import get_user_model as User
from django.shortcuts import get_list_or_404, get_object_or_404, render
# rest framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse

# Create your views here.
# testing urls

# TODO : (Link index to all other places)


def index(request):
    return render(request, 'index.html', {})

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

# ws//:


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

# wss//:


def groupIndex(request):
    return render(request, 'group/index.html', {})


def groupRoom(request, msg_from, grp):
    return render(request, 'group/room.html', {
        'msg_from': msg_from,
        'grp': grp,
    })

# ws//:


def groupIndexTest(request):
    return render(request, 'group/testing/index.html', {})


def groupRoomTest(request, msg_from, grp):
    return render(request, 'group/testing/room.html', {
        'msg_from': msg_from,
        'grp': grp,
    })

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
