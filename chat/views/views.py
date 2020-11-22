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

'''
endpoints to br implemented :

    - get/update last_active (or check if user is active right now)
    - get/update last_received_receiver
    - get/update last_seen_receiver
    - new_user (dialogue)
    - new_grp
    - new_room
'''


# TODO : (Add logic to remove/add users to groups)
