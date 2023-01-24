from rest_framework import routers

from couveflow.core.views import DeviceRegisterViewSet

router = routers.SimpleRouter()
router.register(r'device-register',
                DeviceRegisterViewSet,
                basename="device-register")
