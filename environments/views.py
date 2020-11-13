from rest_framework.generics import get_object_or_404
from rest_framework.serializers import Serializer
from .models import Environments, UserInEnv
from .serializers import EnvironmentsSerializer,UserInEnvSerializer
#from rest_framework import viewsets
#from django.contrib.auth.models import User
from rest_framework import status,mixins,viewsets
#from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User


# Create your views here.
class EnvironmentsViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class=EnvironmentsSerializer
    queryset= Environments.objects.all()
    def list(self, req):
        queryset = Environments.objects.all()
        serializer = EnvironmentsSerializer(queryset, many=True)
        #print(Response(serializer.data))
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Environments.objects.all()
        Environment = get_object_or_404(queryset, pk=pk)
        serializer = EnvironmentsSerializer(Environment)
        return Response(serializer.data)

#@action(detail=True, methods=['post', 'delete']
@api_view(('GET',))
def env(req,name):
    #print(Environments.objects.filter(Name=name)[0].Name)
    #req.pk=Environments.objects.filter(Name=name)[0].id
    queryset = Environments.objects.all()
    #if(len(queryset)==0):RAISE_ERROR
    Environment = get_object_or_404(queryset, Name=name)
    serializer = EnvironmentsSerializer(Environment)
    #print(serializer.data)
    return Response(serializer.data,status=status.HTTP_200_OK)
    #print(req)
    #return Response(req.serializer_class(Environments.objects.filter(Name=name)).data)


class UserInEnvViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,
        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class=UserInEnvSerializer
    queryset= UserInEnv.objects.all()
@api_view(('GET',))
def UserEnv(req):
    print(req.user.pk)
    serializer=UserInEnvSerializer(UserInEnv.objects.filter(User_Key=req.user.pk),many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)