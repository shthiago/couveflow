from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from couveflow.core.constants import INTERACTION_ASK_ACTION
from couveflow.core.guidelines.evaluator import GuidelineEvaluator
from couveflow.core.models import Device
from couveflow.core.serializers import DeviceRegisterSerializer
from couveflow.core.serializers.ask_action import AskActionSerializer
from couveflow.core.views.utils import register_interaction


class ActionsViewSet(ViewSet):
    @action(methods=['get'], detail=False)
    def ask(self, request: Request, declared_id: str):
        device = self._get_device(declared_id)
        actions = device.actions.all()
        evaluator = GuidelineEvaluator()
        matched_actions = [
            {
                'action': action.code,
            } for action in actions
            if evaluator.evaluate(action.expression)
        ]
        serializer = AskActionSerializer(
            data=matched_actions,
            many=True
        )
        serializer.is_valid()
        return Response(
            data=serializer.validated_data,
            status=status.HTTP_200_OK
        )

    def _get_device(self, declared_id: str) -> Device:
        try:
            return Device.objects.get(declared_id=declared_id)

        except Device.DoesNotExist:
            raise NotFound(
                detail=f'Device with declared id `{declared_id}` not found')
