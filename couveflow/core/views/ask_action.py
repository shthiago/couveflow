from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from couveflow.core.constants import INTERACTION_ASK_ACTION
from couveflow.core.guidelines.evaluator import GuidelineEvaluator
from couveflow.core.serializers import AskActionSerializer
from couveflow.core.views.mixins import GetDeviceMixin, GetSerializerMixin
from couveflow.core.views.utils import register_interaction


class ActionsViewSet(ViewSet, GetSerializerMixin, GetDeviceMixin):
    serializer_class = AskActionSerializer

    @action(methods=['get'], detail=False)
    def ask(self, request: Request, declared_id: str):
        device = self.get_device(declared_id)
        actions = device.actions.all()
        evaluator = GuidelineEvaluator()
        matched_actions = [
            {
                'action': action.code,
            } for action in actions
            if evaluator.evaluate(action.expression)
        ]
        serializer = self.get_serializer(
            data=matched_actions,
            many=True
        )

        register_interaction(device, INTERACTION_ASK_ACTION)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
