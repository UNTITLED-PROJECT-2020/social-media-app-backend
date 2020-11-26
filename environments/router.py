from .views import EnvironmentsViewset, UserInEnvViewset
from rest_framework import routers

#router for viewset 'Environments'
#router is a path for accessing certain objects of a viewset
router=routers.DefaultRouter()
router.register('user',UserInEnvViewset,basename='UserInEnv')
router.register('',EnvironmentsViewset,basename='environments')

