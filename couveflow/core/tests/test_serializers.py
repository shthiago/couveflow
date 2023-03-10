from typing import Dict

import pytest

from couveflow.core import serializers
from couveflow.core.models import Action, Device, Measure, Sensor, Variable
from couveflow.core.serializers.measure import MeasureSerializer
from couveflow.core.tests.factories import (DeviceFactory, SensorFactory,
                                            VariableFactory)
from couveflow.tests.factories import UserFactory


@pytest.mark.django_db
class TestActionSerializer:
    @pytest.fixture
    def variable(self):
        return VariableFactory(name='my_var', value=1)

    @pytest.fixture
    def data(self, variable: Variable):
        return {
            'expression': f'var(\'{variable.name}\') == 1',
            'code': 'send_sensor_measure',
            'params': {'key': 'a'},
        }

    def test_correct_serialization(self, data: Dict):
        serializer = serializers.ActionSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_incorrect_expression(self):
        data = {
            'expression': 'not valid expression',
            'code': 'send_sensor_measure',
            'params': {'key': 'a'},
        }

        serializer = serializers.ActionSerializer(data=data)
        assert not serializer.is_valid()

    def test_save_action(self, data: Dict):
        serializer = serializers.ActionSerializer(data=data)
        serializer.is_valid()
        action = serializer.save(device=DeviceFactory())

        assert action.expression == data['expression']
        assert action.code == data['code']


@pytest.mark.django_db
class TestDeviceRegisterSerializer:
    @pytest.fixture
    def variable(self):
        return VariableFactory(name='my_var', value=1)

    @pytest.fixture
    def data(self, variable: Variable):
        user = UserFactory()
        return {
            'declared_id': 'awesome-device',
            'name': 'pe-de-roma',
            'description': 'Monitors for the bonsai',
            'actions': [
                {
                    'expression': f'var(\'{variable.name}\') == 1',
                    'code': 'send_sensor_measure',
                    'params': {'key': 'a'},
                }
            ],
            'owner_id': user.id,
        }

    def test_correct_serialization(self, data: Dict):
        serializer = serializers.DeviceRegisterSerializer(data=data)
        assert serializer.is_valid()

    def test_objects_creation(self, data: Dict):
        serializer = serializers.DeviceRegisterSerializer(data=data)
        assert serializer.is_valid()
        serializer.save()

        assert Device.objects.count() == 1
        device = Device.objects.first()
        assert device.name == data['name']
        assert device.description == data['description']
        assert device.declared_id == data['declared_id']

        assert Action.objects.count() == 1
        action = Action.objects.first()
        assert device.actions.first() == action


@pytest.mark.django_db
class TestMeasureSerializer:
    @pytest.fixture
    def sensor(self):
        return SensorFactory()

    @pytest.fixture
    def data(self, sensor: Sensor):
        return {
            'value': 12.0,
            'sensor': sensor.id,
        }

    def test_measure_creation(self, data: Dict):
        serializer = MeasureSerializer(data=data)
        assert serializer.is_valid()
        serializer.save()

        assert Measure.objects.count() == 1
        measure = Measure.objects.first()
        assert measure.value == data['value']
        assert measure.sensor.id == data['sensor']
