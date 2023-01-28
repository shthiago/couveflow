# Disable abstract-method for serializers since the project does not intend to use
# update method for this serializer yet
# pylint: disable=W0223
from typing import Dict

from rest_framework import serializers

from couveflow.core.models import Device
from couveflow.core.serializers.action import ActionSerializer
from couveflow.core.serializers.exceptions import DeviceRecreationAttempt


class DeviceRegisterSerializer(serializers.Serializer):
    declared_id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    actions = ActionSerializer(many=True)
    owner_id = serializers.IntegerField()

    def create(self, validated_data: Dict):
        actions = validated_data.pop("actions")
        device, created = Device.objects.get_or_create(**validated_data)

        if not created:
            raise DeviceRecreationAttempt()

        action_serializer = ActionSerializer(data=actions, many=True)
        action_serializer.is_valid(raise_exception=True)
        action_serializer.save(device=device)

        return device
