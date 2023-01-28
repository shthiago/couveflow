from rest_framework import permissions
from rest_framework.request import Request

from couveflow.core.models import Device


class IsDeviceOwner(permissions.BasePermission):

    def has_permission(self, request: Request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        device_declared_id = view.kwargs.get('declared_id')
        if not device_declared_id:
            return False

        try:
            device = Device.objects.get(declared_id=device_declared_id)
        except Device.DoesNotExist:
            return False

        return device.owner == request.user
