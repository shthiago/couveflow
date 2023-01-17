from rest_framework import serializers

from couveflow.core.serializers.action import ActionSerializer


class DeviceRegisterSerializer(serializers.Serializer):
    declared_id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    actions = ActionSerializer(many=True)
