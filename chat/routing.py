# chat/routing.py
from django.urls import re_path, path
# from django.conf.urls import patterns, include, url

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/', consumers.ChatConsumer),
]

channel_routing = {}
