# imports
from .views import views, templateViews, chatViews, infoViews
from django.urls import include, path, re_path
# rest framework imports
from rest_framework.routers import DefaultRouter

# connected to 'chat/'
app_name = 'chat'

# urls
urlpatterns = [
    path('', templateViews.index, name="Index Page"),

    ##################################################
    ######## urls for Personal Chats #############
    ##################################################
    path('personal/', templateViews.personalIndex, name="Personal Index"),
    path('personal/<str:msg_from>/<str:msg_to>/',
         templateViews.personalRoom, name="Personal Chat Room"),
    # testing
    path('personal/test', templateViews.personalIndexTest, name="Personal Index"),
    path('personal/test/<str:msg_from>/<str:msg_to>/',
         templateViews.personalRoomTest, name="Personal Chat Room"),

    ##################################################
    ######## urls for Group Chats #############
    ##################################################
    path('group/', templateViews.groupIndex, name="Group Index"),
    path('group/<str:msg_from>/<str:grp>/',
         templateViews.groupRoom, name="Group Chat Room"),
    # testing
    path('group/test', templateViews.groupIndexTest, name="Group Index"),
    path('group/test/<str:msg_from>/<str:grp>/',
         templateViews.groupRoomTest, name="Group Chat Room"),

    ##################################################
    ######## urls for ChatRoom Chats #############
    ##################################################
    path('room/', templateViews.chatRoomIndex, name="Chat Room Index"),
    path('room/<str:room_name>/', templateViews.chatRoom, name="Chat Room"),








    ##################################################
    ######## urls for Special Chats #############
    ##################################################
    path('special/',
         chatViews.GenericSpecialViewSet.as_view({'get': 'list'}), name="Special Index"),
    path('special/<str:generate>/', chatViews.GenericSpecialViewSet.as_view({'post': 'create'}),
         name="Special Generate Chats"),

    ##################################################
    ######## urls for Chats Info #############
    ##################################################
    path('info/', infoViews.GenericInfoViewSet.as_view(
        {'get': 'list'}), name="Info Index"),
    path('info/<str:user_num>/', infoViews.GenericInfoViewSet.as_view({'get': 'retrieve', 'put': 'update'}),
         name="Info Active Details"),
    path('info/<str:msg_from>/<str:msg_to>/',
         infoViews.GenericInfoViewSet.as_view({'get': 'retrieve'}), name="Info Last Read/Seen Details"),
]
