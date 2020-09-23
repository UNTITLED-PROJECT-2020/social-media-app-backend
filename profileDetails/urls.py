# imports
from . import views
<<<<<<< HEAD
from django.urls import include, path, re_path
from django.shortcuts import render


# connected to '/'
app_name = 'profileDetails'


urlpatterns = [
    # path('', views.home, name="home"),
=======
from django.urls import include, path
# rest framework imports
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# connected to 'auth/'
app_name = 'profileDetails'

# # creating router to redirect to
# authRouter = DefaultRouter()
# authRouter.register('signup', views.GenericSignupViewSet, basename="signup")
# authRouter.register(
#     'loginData', views.GenericLoginViewSet, basename="login")

# # urls
urlpatterns = [
    # path('', include(authRouter.urls), name="GenericAuthViewSet"),
    # # returning token using only (username, password)
    # path('login/', obtain_auth_token),
>>>>>>> master
]
