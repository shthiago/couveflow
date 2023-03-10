import pytest

from couveflow.core.models import Sensor
from couveflow.core.tests.factories import DeviceFactory
from couveflow.core.views.utils import get_or_create_sensor


@pytest.mark.django_db
class TestGetSensor:
    def test_get_or_create_sensor(self):
        device = DeviceFactory()
        label = 'my_sensor'

        assert Sensor.objects.count() == 0
        sensor = get_or_create_sensor(device, label)
        assert Sensor.objects.count() == 1
        assert sensor.device == device
        assert sensor.label == label

    def test_re_get_or_create_sensor(self):
        device = DeviceFactory()
        label = 'my_sensor'

        assert Sensor.objects.count() == 0
        get_or_create_sensor(device, label)
        assert Sensor.objects.count() == 1
        get_or_create_sensor(device, label)
        assert Sensor.objects.count() == 1
