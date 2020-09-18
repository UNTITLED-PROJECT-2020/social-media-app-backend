# imports
import json
from .models import Account
from .serializers import AccountSerializer
# rest framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins
from rest_framework import viewsets

# Create your views here.


class GenericLoginViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    # return username if login with any other field (i.e. : phone number, email)
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def create(self, req):  # post method
        data = {}  # creating data dictionary to send as response
        if req.data:
            info = req.data  # putting req.data into info for ease

            # return user account
            if 'username' in info:  # check if username is in request
                account = Account.objects.get(
                    username=info['username'])
            elif 'email' in info:  # check if email is in request
                account = Account.objects.get(email=info['email'])
            elif 'ph_num' in info:  # check if phone number is in request
                account = Account.objects.get(ph_num=info['ph_num'])
            else:  # send error if noting found
                data["error"] = "Incorrect data passed"
                return Response(data, status=status.HTTP_404_NOT_FOUND)

            # creating serializer and sending back data
            serializer = self.serializer_class(account)
            return Response({"username": serializer.data['username']}, status=status.HTTP_200_OK)

        else:
            data["error"] = "no data provided"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class GenericSignupViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    # creating user and returning data with token
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def create(self, req):  # overriding create method

        # creating serializer
        serializer = AccountSerializer(data=req.data)
        data = {}

        if serializer.is_valid(raise_exception=True):  # checking validity
            # saving user account
            account = serializer.save()
            token = Token.objects.get(user=account)

            # appending information to data dictionary JSON
            data['response'] = "success"
            data['data'] = serializer.data
            data['token'] = str('Token ') + str(token)

            statusCode = status.HTTP_201_CREATED  # creating http code

        else:
            data['error'] = "some unexpected error occored"
            statusCode = status.HTTP_400_BAD_REQUEST  # creating http code

        return Response(data, status=statusCode)  # sending data with code

# to add authentication to a view use:
# $ authentication_classes = [TokenAuthentication]
# $ permission_classes = [IsAuthenticated]
