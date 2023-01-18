from typing import Dict
from rest_framework import serializers
from couveflow.core.models import Device

from couveflow.core.serializers.action import ActionSerializer


class DeviceRegisterSerializer(serializers.Serializer):
    declared_id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    actions = ActionSerializer(many=True)

    def create(self, validated_data: Dict):
        actions = validated_data.pop("actions")
        device = Device.objects.create(**validated_data)

        action_serializer = ActionSerializer(data=actions, many=True)
        action_serializer.is_valid(raise_exception=True)
        action_serializer.save(device=device)

        return device
