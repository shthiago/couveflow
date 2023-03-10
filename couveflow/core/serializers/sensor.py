from rest_framework import serializers

from couveflow.core.models import Sensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'label', 'device']
