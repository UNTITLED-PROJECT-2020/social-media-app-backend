# imports
from chat.serializers import GroupSerializer
import json
from ..models import Group, Message, Dialogue, ActiveDetail
from django.contrib.auth import get_user_model as User
from django.shortcuts import get_object_or_404
# rest framework imports
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from django.http import JsonResponse

# Create your views here.


class GenericPersonalInfoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    def list(self, req, *args, **kwargs):
        pass

    def create(self, req, *args, **kwargs):
        pass

    def update(self, req, *args, **kwargs):
        pass

    def retrieve(self, req, *args, **kwargs):
        data = req.data
        info = {}

        # get seen/receive details
        msg_from = get_object_or_404(User(), ph_num=data['msg_from'])
        msg_to = get_object_or_404(User(), ph_num=data['msg_to'])
        dialogue = get_object_or_404(
            Dialogue, sender=msg_from, receiver=msg_to)

        info["last_received_receiver"] = dialogue.last_received_receiver
        info["last_seen_receiver"] = dialogue.last_seen_receiver
        info['info'] = 'returned'
        stat = status.HTTP_302_FOUND

        return JsonResponse(info, safe=False, status=stat)

    def delete(self, req, *args, **kwargs):
        pass


class GenericGroupInfoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    def list(self, req, *args, **kwargs):
        pass

    def create(self, req, *args, **kwargs):
        pass

    def update(self, req, *args, **kwargs):
        pass

    def retrieve(self, req, *args, **kwargs):
        data = req.data
        info = {}

        # get group details
        grp = get_object_or_404(Group, key=data['grp_name'])

        info = GroupSerializer(grp).data
        info['info'] = 'returned'

        stat = status.HTTP_302_FOUND

        return JsonResponse(info, safe=False, status=stat)

    def delete(self, req, *args, **kwargs):
        pass


class GenericRoomInfoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    def list(self, req, *args, **kwargs):
        pass

    def create(self, req, *args, **kwargs):
        pass

    def update(self, req, *args, **kwargs):
        pass

    def retrieve(self, req, *args, **kwargs):
        pass

    def delete(self, req, *args, **kwargs):
        pass


class GenericSpecialInfoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    def list(self, req, *args, **kwargs):
        pass

    def create(self, req, *args, **kwargs):
        pass

    def update(self, req, *args, **kwargs):
        pass

    def retrieve(self, req, *args, **kwargs):
        pass

    def delete(self, req, *args, **kwargs):
        pass


class GenericActiveInfoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    def list(self, req, *args, **kwargs):
        pass

    def create(self, req, *args, **kwargs):
        pass

    def update(self, req, *args, **kwargs):
        data = req.data
        info = {}

        detial = get_object_or_404(
            User(), ph_num=data['user_num']).activeDetail

        if (data['command'] == 'activate'):
            detial.active = True
            detial.last_active = data['last_active']
            detial.save()

            info['info'] = "updated"
            info['message'] = "Active Data Has been updated"

            stat = status.HTTP_200_OK

        elif (data['command'] == 'deactivate'):
            detial.active = False
            detial.last_active = data['last_active']
            detial.save()

            info['info'] = "updated"
            info['message'] = "Active Data Has been updated"

            stat = status.HTTP_200_OK

        else:
            info['info'] = "error"
            info['message'] = "incorrect request/url"

            stat = status.HTTP_400_BAD_REQUEST

        return JsonResponse(info, safe=False, status=stat)

    def retrieve(self, req, *args, **kwargs):
        data = req.data
        info = {}

        # get active details
        detail = get_object_or_404(
            User(), ph_num=data['user_num']).activeDetail

        info["info"] = "found"
        info["active"] = detail.active
        info["last_active"] = detail.last_active

        stat = status.HTTP_302_FOUND

        return JsonResponse(info, safe=False, status=stat)

    def delete(self, req, *args, **kwargs):
        pass
