from rest_framework import serializers

from couveflow.core.models import Device, Measure
from couveflow.core.serializers.exceptions import DeviceNotFound


class MeasureSerializer(serializers.ModelSerializer):
    device_declared_id = serializers.CharField()

    class Meta:
        model = Measure
        fields = ['value', 'source_label', 'device_declared_id']

    def create(self, validated_data: dict):
        """Fill the device field of data before trying to create"""
        try:
            validated_data['device'] = Device.objects.get(
                declared_id=validated_data.pop('device_declared_id'))

        except Device.DoesNotExist as exc:
            raise DeviceNotFound() from exc

        return super().create(validated_data)
