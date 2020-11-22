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


class GenericSpecialViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # create different types of chat and render index

    def list(self, req, *args, **kwargs):
        # render index page
        return render(req, 'special/index.html', {})

    def create(self, req, *args, **kwargs):

        generate = self.kwargs['generate']
        data = req.data

        # configuring which type of request is sent

        if (generate == "personal"):
            # create personal dialogue

            info = {}
            msg_from = get_object_or_404(User(), ph_num=data['msg_from'])
            msg_to = get_object_or_404(User(), ph_num=data['msg_to'])

            # generate a dailogue to send message
            info["msg_from"], from_created = Dialogue.objects.get_or_create(
                sender=msg_from, receiver=msg_to)
            info["msg_to"], to_created = Dialogue.objects.get_or_create(
                sender=msg_to, receiver=msg_from)

            if from_created and to_created:
                info['info'] = 'created'
            else:
                info['info'] = 'returned'

            info["msg_from"] = info["msg_from"].sender.ph_num
            info["msg_to"] = info["msg_to"].sender.ph_num

            # info["msg_from"]
            print(info)

            return JsonResponse(info, safe=False)

        elif (generate == "group"):     # create group dialogue

            # grp_name, bio, admin, participants
            while True:
                grp_key = uuid.uuid4().hex[:11].upper()

                group, created = Group.objects.get_or_create(key=grp_key)

                if created:
                    break
                else:
                    pass

            group.name = data['grp_name']
            group.bio = data['bio']

            for user in data['admin']:
                group.admin.add(User().objects.get(ph_num=user))

                if user not in data['participants']:
                    data['participants'].append(user)

            for user in data['participants']:
                group.participants.add(User().objects.get(ph_num=user))

            group.save()

            return JsonResponse(GroupSerializer(group).data, safe=False)

        elif (generate == "room"):  # create room dialogue
            # get active details
            # TODO : (Create Room Chat)
            # data = Dialogue.objects.get(sender=msg_from, receiver=msg_to)
            return JsonResponse(data, safe=False)
        else:   # Send 404 error
            err = {
                "err": "incorrect url",
            }
            return JsonResponse(err, status=status.HTTP_404_NOT_FOUND)
