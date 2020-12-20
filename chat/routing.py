# chat/routing.py
from django.urls import re_path, path
# from django.conf.urls import patterns, include, url

from . import consumers

from chat.consumers.group import ChatGroupConsumer
from chat.consumers.personal import ChatPersonalConsumer
from chat.consumers.room import ChatRoomConsumer
from chat.consumers.special import ChatSpecialConsumer

websocket_urlpatterns = [
    # personal chat
    re_path(r'ws/chat/personal/(?P<msg_from>\w+)/(?P<msg_to>\w+)/',
            ChatPersonalConsumer),

    # group chat
    re_path(r'ws/chat/group/(?P<msg_from>\w+)/(?P<grp_name>\w+)/',
            ChatGroupConsumer),

    # chat room
    re_path(r'ws/chat/room/(?P<msg_from>\w+)/',
            ChatRoomConsumer),

    # special cases
    re_path(r'ws/chat/special/(?P<user_num>\w+)/',
            ChatSpecialConsumer),
]

channel_routing = {}
