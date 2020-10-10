# chat/routing.py
from django.urls import re_path, path
# from django.conf.urls import patterns, include, url

from . import consumers

websocket_urlpatterns = [
    # personal chat
    re_path(r'ws/chat/personal/(?P<msg_from>\w+)/(?P<msg_to>\w+)/',
            consumers.ChatPersonalConsumer),

    # group chat
    re_path(r'ws/chat/group/(?P<msg_from>\w+)/(?P<group_name>\w+)/',
            consumers.ChatGroupConsumer),

    # chat room
    re_path(r'ws/chat/room/(?P<room_name>\w+)/',
            consumers.ChatRoomConsumer),

    # special cases
    re_path(r'ws/chat/special/(?P<user_num>\w+)/',
            consumers.ChatSpecialConsumer),
]

channel_routing = {}
