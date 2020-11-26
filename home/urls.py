# imports
from . import views
from django.urls import include, path, re_path
from django.shortcuts import render


# connected to '/'
app_name = 'home'


urlpatterns = [
    path('', views.home, name="home"),
    path('start.html/', views.start, name="start"),
    path('components.html/', views.components, name="components"),
    path('charts.html/', views.charts, name="charts"),
    path('faqs.html/', views.faqs, name="faqs"),
    path('showcase.html/', views.showcase, name="showcase"),
    path('license.html/', views.license, name="license"),
]
