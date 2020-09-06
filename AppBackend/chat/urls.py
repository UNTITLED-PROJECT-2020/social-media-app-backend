# imports
from . import views
from django.urls import include, path
# rest framework imports
from rest_framework.routers import DefaultRouter

# connected to 'auth/'
app_name = 'chat'

# creating router to redirect to
authRouter = DefaultRouter()

# urls
urlpatterns = []
