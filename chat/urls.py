# imports
from .views import chatViews, infoViews
from .views.templateViews import index, personal, group, room, special, info
from django.urls import path
# rest framework imports
from rest_framework.routers import DefaultRouter

# connected to 'chat/'
app_name = 'chat'

# dictionary of all the generic methods
method_dict = {
    #     'get': 'list',
    'post': 'create',
    'put': 'update',
    'patch': 'retrieve',
    'delete': 'delete',
}

# urls
urlpatterns = [

    ##########################################
    ######## urls for Chat Index #############
    ##########################################

    path('',
         index, name="Index Page"),

    path('personal/<str:msg_from>/<str:msg_to>/',
         personal, name="Personal Chat Room"),

    path('group/<str:msg_from>/<str:grp>/',
         group, name="Group Chat Room"),

    path('room/<str:msg_from>/',
         room, name="Chat Room"),

    # TODO : (define urls for special and info)

        #     path('special/',
        #          special, name="Chat Room"),

    path('info/',
         info, name="Chat Room"),


    ###############################################################
    ######## urls for creating/updating/deleting Chat #############
    ###############################################################

    path('special/personal/',
         chatViews.GenericPersonalViewSet.as_view(method_dict),
         name="Personal Views"),

    path('special/group/',
         chatViews.GenericGroupViewSet.as_view(method_dict),
         name="Group Views"),

        #     path('special/room/',
        #          chatViews.GenericRoomViewSet.as_view(method_dict),
        #          name="Room Views"),

        #     path('special/special/',
        #          chatViews.GenericSpecialViewSet.as_view(method_dict),
        #          name="Special Views"),


    ##################################################
    ######## urls for getting Chat Info #############
    ##################################################

    path('info/personal/',
         infoViews.GenericPersonalInfoViewSet.as_view(method_dict),
         name="Info Personal Details"),

    path('info/group/',
         infoViews.GenericGroupInfoViewSet.as_view(method_dict),
         name="Info Group Details"),

        #     path('info/room/',
        #          infoViews.GenericRoomInfoViewSet.as_view(method_dict),
        #          name="Info Room Details"),

        #     path('info/special/',
        #          infoViews.GenericSpecialInfoViewSet.as_view(method_dict),
        #          name="Info Special Details"),

    path('info/active/',
         infoViews.GenericActiveInfoViewSet.as_view(method_dict),
         name="Info Active Details"),
]
