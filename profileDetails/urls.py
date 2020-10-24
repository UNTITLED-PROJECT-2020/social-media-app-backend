# imports
from . import views
from django.urls import include, path, re_path
from django.shortcuts import render


# connected to '/'
app_name = 'profileDetails'


urlpatterns = [
    # path('', views.home, name="home"),
    path('AccountDetail/', views.ProfileViewsets),
]
