from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from couveflow.core.constants import INTERACTION_REGISTER_DEVICE
from couveflow.core.serializers import DeviceRegisterSerializer
from couveflow.core.views.mixins import GetSerializerMixin
from couveflow.core.views.utils import register_interaction


class DeviceRegisterViewSet(ViewSet, GetSerializerMixin):
    serializer_class = DeviceRegisterSerializer

    def create(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        device = serializer.save()
        register_interaction(device, INTERACTION_REGISTER_DEVICE)
        return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
