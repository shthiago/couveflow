from rest_framework import routers

from couveflow.core.views import (ActionsViewSet, DeviceRegisterViewSet,
                                  MeasureViewSet)

router = routers.SimpleRouter()
router.register(
    r'devices/register',
    DeviceRegisterViewSet,
    basename="devices-register"
)
router.register(
    r'devices/(?P<declared_id>[\w]+)/actions',
    ActionsViewSet,
    basename="devices-actions"
)
router.register(
    r'devices/(?P<declared_id>[\w]+)/measures',
    MeasureViewSet,
    basename="devices-measures"
)

urlpatterns = router.urls
