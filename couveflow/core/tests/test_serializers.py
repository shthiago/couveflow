from typing import Dict
import pytest

from couveflow.core import serializers
from couveflow.core.models import Action, Device, Measure, Variable
from couveflow.core.serializers.exceptions import DeviceNotFound
from couveflow.core.serializers.measure import MeasureSerializer
from couveflow.core.tests.factories import DeviceFactory, VariableFactory


@pytest.mark.django_db
class TestActionSerializer:
    @pytest.fixture
    def variable(self):
        return VariableFactory(name="my_var", value=1)

    @pytest.fixture
    def data(self, variable: Variable):
        return {
            "expression": f"var('{variable.name}') == 1",
            "code": "send_sensor_measure"
        }

    def test_correct_serialization(self, data: Dict):
        serializer = serializers.ActionSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_incorrect_expression(self):
        data = {
            "expression": "not valid expression",
            "code": "send_sensor_measure"
        }

        serializer = serializers.ActionSerializer(data=data)
        assert not serializer.is_valid()

    def test_save_action(self, data: Dict):
        serializer = serializers.ActionSerializer(data=data)
        serializer.is_valid()
        action = serializer.save(device=DeviceFactory())

        assert action.expression == data["expression"]
        assert action.code == data["code"]


@pytest.mark.django_db
class TestDeviceRegisterSerializer:
    @pytest.fixture
    def variable(self):
        return VariableFactory(name="my_var", value=1)

    @pytest.fixture
    def data(self, variable: Variable):
        return {
            "declared_id": "awesome-device",
            "name": "pe-de-roma",
            "description": "Monitors for the bonsai",
            "actions": [
                {
                    "expression": f"var('{variable.name}') == 1",
                    "code": "send_sensor_measure"
                }
            ]
        }

    def test_correct_serialization(self, data: Dict):
        serializer = serializers.DeviceRegisterSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_objects_creation(self, data: Dict):
        serializer = serializers.DeviceRegisterSerializer(data=data)
        assert serializer.is_valid()
        serializer.save()

        assert Device.objects.count() == 1
        device = Device.objects.first()
        assert device.name == data["name"]
        assert device.description == data["description"]
        assert device.declared_id == data["declared_id"]

        assert Action.objects.count() == 1
        action = Action.objects.first()
        assert device.actions.first() == action


@pytest.mark.django_db
class TestMeasureSerializer:
    @pytest.fixture
    def device(self):
        return DeviceFactory()

    @pytest.fixture
    def data(self, device: Device):
        return {
            'value': 12.0,
            'device_declared_id': device.declared_id,
            'source_label': 'my_awesome_sensor'
        }

    def test_measure_creation(self, data: Dict):
        serializer = MeasureSerializer(data=data)
        assert serializer.is_valid()
        serializer.save()

        assert Measure.objects.count() == 1
        measure = Measure.objects.first()
        assert measure.value == data['value']
        assert measure.source_label == data['source_label']
        assert measure.device.declared_id == data['device_declared_id']

    def test_measure_creation_device_not_found(self, data: Dict):
        fail_data = data.copy()
        fail_data['device_declared_id'] = 'imprettysureitdoesnotexist'
        serializer = MeasureSerializer(data=fail_data)

        assert serializer.is_valid()

        with pytest.raises(DeviceNotFound):
            serializer.save()

        assert Measure.objects.count() == 0
