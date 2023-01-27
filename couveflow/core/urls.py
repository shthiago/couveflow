from rest_framework import routers

from couveflow.core.views import DeviceRegisterViewSet, ActionsViewSet, MeasureViewSet

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
router.register(
    r'devices/measures/(?P<declared_id>[\w]+)',
    MeasureViewSet,
    basename="devices-measures"
)

urlpatterns = router.urls
