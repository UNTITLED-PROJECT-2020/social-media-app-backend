from .models import AccountDetail,Ledger
from .serializers import AccountDetailSerializer,LedgerSerializer
#from rest_framework import viewsets
#from django.contrib.auth.models import User
from rest_framework import mixins,viewsets
#from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from chat.models import Dialogue,Room
import random
from authentication.models import Account
from chat.views.chatViews import GenericRoomViewSet
from rest_framework.decorators import api_view

# Create your views here.
class AccountDetailViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class=AccountDetailSerializer
    queryset= AccountDetail.objects.all()

    def create(self,req):
        if(req.user.pk==None):return Response("Check Token attached",status=status.HTTP_400_BAD_REQUEST)
        if(len(AccountDetail.objects.filter(account=req.user.pk))==1):return Response("Profile Already Exsists",status=status.HTTP_400_BAD_REQUEST)
        req.data['account']=req.user #print(req.data) updating foreignkey from body to header's token
        serializer = self.serializer_class(data=req.data) #Account.objects.filter(pk=req.user.pk)  serialziing the input data
        serializer.is_valid(raise_exception=True) #raising exception for bad data
        temp = serializer.validated_data   #getting the valid data as ordered dict
        self.account=temp.get('account')  #saving all instances
        self.fname=temp.get('fname')
        self.lname=temp.get('lname')
        self.bio=temp.get('bio')
        self.score=temp.get('score')
        serializer.save()
        return Response("Success Account Detail Created",status=status.HTTP_201_CREATED)

class LedgerViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class=LedgerSerializer
    
    queryset= Ledger.objects.all()

    def create(self,req):
        # print(self.request)
        # print(req)
        if(req.user.pk==None):return Response("Check Token attached",status=status.HTTP_400_BAD_REQUEST)
        back={'status':'','recommended':[],"random":[]}
        if(len(Ledger.objects.filter(account=req.user.pk))==1):
            Ledger.objects.filter(account=req.user.pk)[0].delete()
            back['status']='Deleted and '
        Score=AccountDetail.objects.filter(account=req.user.pk)[0].score
        serializer=LedgerSerializer(data={'account':req.user.pk,'env':req.data.get('environment'),
        'score':Score,'ph_num':req.user.ph_num})
        serializer.is_valid(raise_exception=True)
        set=Ledger.objects.filter(
            env=req.data.get('environment')).exclude(
            account__in=[instance.receiver for instance in Dialogue.objects.filter(sender=req.user)])
        UsersToBeExcluded=[]
        for instance in Room.objects.filter(participants=req.user):
            UsersToBeExcluded.append(instance.participants.all()[0])
            UsersToBeExcluded.append(instance.participants.all()[0])
        set=set.exclude(
             account__in=UsersToBeExcluded)
        # print(set)
        set=set.filter(score__lte=Score)
        set=set.exclude(score__lte=Score-15)
        count=0
        for item in set:
            if(count==10):break
            count+=1
            back['recommended'].append(item.account.pk)
        if(len(set)==0):return Response(back,status=status.HTTP_201_CREATED)
        back['random']=[random.choice(set).account.pk]
        back['status']+='Created'
        serializer.save()
        return Response(back,status=status.HTTP_201_CREATED)

def scoreAdjust(ph_num,change):
    AccountDetail.objects.filter(account=Account.objects.filter(ph_num=ph_num)[0].pk)[0].score+=change
    # @api_view(('POST',))
    # def match(req):
    #     data=req.data
    #     Ledger.objects.filter(account=Account.objects.filter(ph_num=req.data.get('msg_from'))[0].pk)[0].delete()
    #     Ledger.objects.filter(account=Account.objects.filter(ph_num=req.data.get('msg_to'))[0].pk)[0].delete()
    #     GenericRoomViewSet.create(req)