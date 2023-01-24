from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from couveflow.core.serializers import DeviceRegisterSerializer
from couveflow.core.models import Device


class DeviceRegisterViewSet(ViewSet):
    serializer_class = DeviceRegisterSerializer
    queryset = Device.objects.all()

    def get_serializer(self, *args, **kwargs) -> DeviceRegisterSerializer:
        serializer = self.serializer_class(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer

    def create(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.save()
        return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
