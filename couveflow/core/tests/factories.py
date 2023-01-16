from datetime import datetime
from factory.django import DjangoModelFactory
from factory import SubFactory, LazyAttribute
from couveflow.core import models


class VariableFactory(DjangoModelFactory):
    class Meta:
        model = models.Variable

    name = 'pizza?'
    value = 'yes'


class DeviceFactory(DjangoModelFactory):
    class Meta:
        model = models.Device

    declared_id = "my_awesome_device"
    name = "My awesome monitoring device"
    description = "Measuring anything around"


class InteractionFactory(DjangoModelFactory):
    class Meta:
        model = models.Interaction

    device = SubFactory(DeviceFactory)
    created = LazyAttribute(datetime.now)


class MeasureFactory(DjangoModelFactory):
    class Meta:
        model = models.Measure

    device = SubFactory(DeviceFactory)
    created = LazyAttribute(datetime.now)
    source_label = "any_label"
    value = 42
