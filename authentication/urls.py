# imports
from . import views
from django.urls import include, path
# rest framework imports
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# connected to 'auth/'
app_name = 'authentication'

# dictionary of all the generic methods
method_dict = {
    #     'get': 'list',
    'post': 'create',
    # 'put': 'update',
    # 'patch': 'retrieve',
    # 'delete': 'delete',
}

# urls
urlpatterns = [
    # returning token using only (username, password)
    path('login/', obtain_auth_token),

    # signing up
    path('signup/', views.GenericSignupViewSet.as_view(method_dict), name="signup"),

    # returning data
    path('loginData/', views.GenericLoginViewSet.as_view(method_dict), name="login"),
]
