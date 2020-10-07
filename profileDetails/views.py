import json
from .models import AccountDetail
from .serializers import AccountDetailSerializer
from django.shortcuts import render
#from rest_framework import viewsets
#from django.contrib.auth.models import User
from rest_framework import generics,mixins,viewsets
#from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

# Create your views here.
class AccountDetailViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class=AccountDetailSerializer
    queryset= AccountDetail.objects.all()   