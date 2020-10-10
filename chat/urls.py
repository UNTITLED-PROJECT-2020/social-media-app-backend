# imports
from . import views
from django.urls import include, path, re_path
# rest framework imports
from rest_framework.routers import DefaultRouter

# connected to 'auth/'
app_name = 'chat'

# creating router to redirect to
authRouter = DefaultRouter()

# urls
urlpatterns = [
    ##################################################
    ######## urls for Personal Chats #############
    ##################################################
    path('personal/', views.personalIndex, name="Personal Index"),
    path('personal/<str:msg_from>/<str:msg_to>/',
         views.personalRoom, name="Personal Chat Room"),

    ##################################################
    ######## urls for Group Chats #############
    ##################################################

    ##################################################
    ######## urls for ChatRoom Chats #############
    ##################################################
    path('room/', views.chatRoomIndex, name="Chat Room Index"),
    path('room/<str:room_name>/', views.chatRoom, name="Chat Room"),

    ##################################################
    ######## urls for Special Chats #############
    ##################################################
]
