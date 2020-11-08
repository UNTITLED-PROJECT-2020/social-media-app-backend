import json
from .models import Environments
from .serializers import EnvironmentsSerializer
from django.shortcuts import render
#from rest_framework import viewsets
from django.contrib.auth.models import User
#from django.contrib.auth.models import User
from rest_framework import generics,mixins,viewsets
#from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from authentication.models import Account

# Create your views here.
class EnvironmentsViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class=EnvironmentsSerializer
    queryset= Environments.objects.all()
