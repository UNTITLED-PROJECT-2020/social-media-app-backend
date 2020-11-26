# imports
from . import views
from django.urls import include, path, re_path
from django.shortcuts import render
from .router import router

# connected to '/'
app_name = 'environments'

urlpatterns = [
    path('join/',views.join),
    path('name/<str:name>/',views.env),
    path('userenv/',views.UserEnv),
    path('',include((router.urls,'/'),namespace='environments')),
]
