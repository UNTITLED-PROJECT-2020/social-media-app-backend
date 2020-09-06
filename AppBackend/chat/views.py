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
