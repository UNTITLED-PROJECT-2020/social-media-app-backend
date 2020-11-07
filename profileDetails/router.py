from .views import AccountDetailViewset
from rest_framework import routers

#router for viewset 'AccountDetail'
#router is a path for accessing certain objects of a viewset
router=routers.DefaultRouter()
router.register('',AccountDetailViewset)