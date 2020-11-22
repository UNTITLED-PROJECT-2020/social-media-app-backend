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


class GenericInfoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    # retrieve different types of chat information, render index and update time information
    # serializer_class = ActiveDetail
    # queryset = ActiveDetail.objects.all()

    def list(self, req, *args, **kwargs):
        # render index page
        return render(req, 'info/index.html', {})

    def retrieve(self, req, *args, **kwargs):

        try:
            user_num = self.kwargs['user_num']
        except:
            user_num = None

        try:
            msg_from = self.kwargs['msg_from']
            msg_to = self.kwargs['msg_to']
        except:
            msg_from = None
            msg_to = None

        print(user_num == None, msg_from, msg_to)
        if user_num is None:
            print("mahshallah")
        # configuring which type of request is sent

        if (msg_from == None and msg_to == None):
            # get active details
            try:
                data = get_object_or_404(User(), ph_num=user_num).activeDetail
                info = {}
                info["active"] = data.active
                info["last_active"] = data.last_active
            except:
                err = {
                    "err": "Active Details Not Found",
                }
                # data = User().objects.get(ph_num=user_num).activeDetail
                return JsonResponse(err, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse({"data": info}, safe=False, status=status.HTTP_302_FOUND)
        elif user_num is None:
            # get seen/receive details
            data = get_object_or_404(
                Dialogue,
                sender=User().objects.get(ph_num=msg_from),
                receiver=User().objects.get(ph_num=msg_to))
            info = {}
            info["last_received_receiver"] = data.last_received_receiver
            info["last_seen_receiver"] = data.last_seen_receiver
            return JsonResponse(info, safe=False, status=status.HTTP_302_FOUND)

        else:
            err = {
                "err": "incorrect url",
            }
            return JsonResponse(err, status=status.HTTP_404_NOT_FOUND)

    def update(self, req, *args, **kwargs):

        user_num = self.kwargs['user_num']
        data = req.data

        if (data['command'] == 'activate'):
            info = get_object_or_404(User(), ph_num=user_num).activeDetail

            info.active = True
            info.last_active = data['last_active']
            info.save()

            return JsonResponse({"Response": "Data Updated"}, safe=False, status=status.HTTP_200_OK)

        elif (data['command'] == 'deactivate'):
            info = get_object_or_404(User(), ph_num=user_num).activeDetail

            info.active = False
            info.last_active = data['last_active']
            info.save()

            return JsonResponse({"Response": "Data Updated"}, safe=False, status=status.HTTP_200_OK)

        else:
            err = {
                "err": "incorrect request/url",
            }
            return JsonResponse(err, status=status.HTTP_404_NOT_FOUND)
