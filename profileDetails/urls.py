# imports
from . import views
from django.urls import include, path, re_path
from django.shortcuts import render
from .router import router

# connected to '/'
app_name = 'profileDetails'

urlpatterns = [
    path('',include((router.urls,'Account Details'),namespace='Account Detail')),
]
