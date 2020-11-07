import json
from .models import AccountDetail
from .serializers import AccountDetailSerializer
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
class AccountDetailViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class=AccountDetailSerializer
    queryset= AccountDetail.objects.all()

    def create(self,req):
        if(req.user.pk==None):return Response("Check Token attached",status=status.HTTP_400_BAD_REQUEST)
        if(len(AccountDetail.objects.filter(Account=req.user.pk))==1):return Response("Profile Already Exsists",status=status.HTTP_400_BAD_REQUEST)
        req.data['Account']=req.user.pk #print(req.data) updating foreignkey from body to header's token
        serializer = self.serializer_class(data=req.data) #Account.objects.filter(pk=req.user.pk)  serialziing the input data
        serializer.is_valid(raise_exception=True) #raising exception for bad data
        temp = serializer.validated_data   #getting the valid data as ordered dict
        self.Account=temp.get('Account')  #saving all instances
        self.fname=temp.get('fname')
        self.lname=temp.get('lname')
        self.bio=temp.get('bio')
        self.score=temp.get('score')
        serializer.save()
        return Response("Success Account Detail Created",status=status.HTTP_201_CREATED)

