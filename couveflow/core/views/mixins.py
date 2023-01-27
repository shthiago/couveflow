from rest_framework.exceptions import NotFound

from couveflow.core.models import Device


class GetSerializerMixin:
    def get_serializer(self, *args, **kwargs):
        serializer = self.serializer_class(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer


class GetDeviceMixin:
    def get_device(self, declared_id: str) -> Device:
        try:
            return Device.objects.get(declared_id=declared_id)

        except Device.DoesNotExist as exc:
            raise NotFound(
                detail=f'Device with declared id `{declared_id}` not found') from exc
