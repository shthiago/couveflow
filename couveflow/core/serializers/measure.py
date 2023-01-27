from rest_framework import serializers

from couveflow.core.models import Measure
from .device import DeviceSerializer


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ['value', 'source_label', 'device']

    def to_representation(self, instance: Measure):
        return {
            'source_label': instance.source_label,
            'value': instance.value,
            'device': DeviceSerializer(instance.device).data
        }
