from .views import EnvironmentsViewset
from rest_framework import routers

#router for viewset 'Environments'
#router is a path for accessing certain objects of a viewset
router=routers.DefaultRouter()
router.register('',EnvironmentsViewset)
