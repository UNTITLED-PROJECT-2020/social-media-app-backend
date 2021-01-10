# imports
from . import views
from django.urls import include, path, re_path
from django.shortcuts import render
from .router import router

# connected to '/'
app_name = 'profileDetails'

urlpatterns = [
    # path('ledger/match/',views.LedgerViewset.match),
    path('',include((router.urls,'/'),namespace='Account Detail')),
]
