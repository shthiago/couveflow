# pylint: disable=R0903,E0213,W0613
import graphene
from graphene_django.types import DjangoObjectType

from couveflow.core.models import Device, Measure, Sensor


class MeasureNode(DjangoObjectType):
    class Meta:
        model = Measure
        fields = '__all__'


class SensorNode(DjangoObjectType):
    measures = graphene.List(
        MeasureNode,
    )

    class Meta:
        model = Sensor
        fields = '__all__'

    @staticmethod
    def resolve_measures(parent, info, **kwargs):
        queryset = parent.measures.all()
        if kwargs:
            queryset = queryset.filter(**kwargs)

        return queryset


class DeviceNode(DjangoObjectType):
    sensors = graphene.List(
        SensorNode,
        label=graphene.String(),
    )

    class Meta:
        model = Device
        fields = '__all__'

    @staticmethod
    def resolve_sensors(parent, info, **kwargs):
        queryset = parent.sensors.all()
        if kwargs:
            queryset = queryset.filter(**kwargs)

        return queryset


class Query(graphene.ObjectType):
    devices = graphene.List(
        DeviceNode,
        declared_id=graphene.String(),
    )

    @staticmethod
    def resolve_devices(parent, info, **kwargs):
        queryset = Device.objects.all()
        if kwargs:
            queryset = queryset.filter(**kwargs)

        return queryset


schema = graphene.Schema(query=Query)
