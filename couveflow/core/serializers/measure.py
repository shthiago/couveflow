from rest_framework import serializers

from couveflow.core.models import Measure


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ['value', 'source_label', 'device']
