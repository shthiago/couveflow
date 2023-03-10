from datetime import datetime

import factory

from couveflow.core import models
from couveflow.tests.factories import UserFactory


class VariableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Variable

    name = 'pizza?'
    value = 'yes'


class DeviceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Device

    declared_id = "my_awesome_device"
    name = "My awesome monitoring device"
    description = "Measuring anything around"
    owner = factory.SubFactory(UserFactory)


class ActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Action


class InteractionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Interaction

    device = factory.SubFactory(DeviceFactory)
    created = factory.LazyAttribute(datetime.now)


class SensorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Sensor

    device = factory.SubFactory(DeviceFactory)
    label = "any_label"


class MeasureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Measure

    sensor = factory.SubFactory(SensorFactory)
    value = 42
