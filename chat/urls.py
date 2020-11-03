# imports
from . import views
from django.urls import include, path, re_path
# rest framework imports
from rest_framework.routers import DefaultRouter

# connected to 'auth/'
app_name = 'chat'

# urls
urlpatterns = [
    ##################################################
    ######## urls for Personal Chats #############
    ##################################################
    path('personal/', views.personalIndex, name="Personal Index"),
    path('personal/<str:msg_from>/<str:msg_to>/',
         views.personalRoom, name="Personal Chat Room"),
    # testing
    path('personal/test', views.personalIndexTest, name="Personal Index"),
    path('personal/test/<str:msg_from>/<str:msg_to>/',
         views.personalRoomTest, name="Personal Chat Room"),

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
    path('special/',
         views.GenericSpecialViewSet.as_view({'get': 'list'}), name="Special Index"),
    path('special/<str:generate>/', views.GenericSpecialViewSet.as_view({'post': 'create'}),
         name="Special Generate Chats"),

    ##################################################
    ######## urls for Chats Info #############
    ##################################################
    path('info/', views.GenericInfoViewSet.as_view(
        {'get': 'list'}), name="Info Index"),
    path('info/<str:user_num>/', views.GenericInfoViewSet.as_view({'get': 'retrieve', 'put': 'update'}),
         name="Info Active Details"),
    path('info/<str:msg_from>/<str:msg_to>/',
         views.GenericInfoViewSet.as_view({'get': 'retrieve'}), name="Info Last Read/Seen Details"),
]
