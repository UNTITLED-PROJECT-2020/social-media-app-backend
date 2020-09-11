# imports
import json
from django.utils.safestring import mark_safe
# rest framework imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins
from rest_framework import viewsets

# Create your views here.


class GenericMessageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    # return username if login with any other field (i.e. : phone number, email)

    def create(self, req):  # post method
        data = {}  # creating data dictionary to send as response
        if req.data:

        else:
            data["error"] = "no data provided"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
