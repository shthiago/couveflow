from django.urls import path
from rest_framework import routers

from couveflow.core.views import DeviceRegisterViewSet, ActionsViewSet

router = routers.SimpleRouter()
router.register(
    r'devices/register',
    DeviceRegisterViewSet,
    basename="devices-register"
)
router.register(
    r'devices/actions/(?P<declared_id>[\w]+)',
    ActionsViewSet,
    basename="devices-actions"
)

urlpatterns = router.urls
