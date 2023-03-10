from rest_framework import serializers

from couveflow.core.models import Measure

from .sensor import SensorSerializer


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ['value', 'sensor']

    def to_representation(self, instance: Measure):
        return {
            'value': instance.value,
            'sensor': SensorSerializer(instance.sensor).data
        }
