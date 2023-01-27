from rest_framework import serializers

from couveflow.core.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'declared_id', 'name', 'description']
