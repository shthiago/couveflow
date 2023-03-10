from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from couveflow.core.constants import INTERACTION_SAVE_MEASURE
from couveflow.core.serializers import MeasureSerializer
from couveflow.core.views.mixins import GetDeviceMixin, GetSerializerMixin
from couveflow.core.views.permissions import IsDeviceOwner
from couveflow.core.views.utils import (get_or_create_sensor,
                                        register_interaction)


class MeasureViewSet(ViewSet, GetSerializerMixin, GetDeviceMixin):
    serializer_class = MeasureSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsDeviceOwner]

    @action(methods=['post'], detail=False)
    def register(self, request: Request, declared_id: str):
        device = self.get_device(declared_id)
        sensor = get_or_create_sensor(
            device=device,
            label=request.data.get('source_label')
        )
        serializer = self.get_serializer(data={
            'value': request.data.get('value'),
            'sensor': sensor.id,
        })
        serializer.save()
        register_interaction(device, INTERACTION_SAVE_MEASURE)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
