import pytest

from couveflow.core import serializers
from couveflow.core.tests.factories import VariableFactory


@pytest.mark.django_db
class TestActionSerializer:
    def test_correct_serialization(self):
        VariableFactory(name="my_var", value=1)
        data = {
            "expression": "var('my_var') == 1",
            "code": "send_sensor_measure"
        }

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


@pytest.mark.django_db
class TestDeviceRegisterSerializer:
    def test_correct_serialization(self):
        VariableFactory(name="my_var", value=1)
        data = {
            "declared_id": "awesome-device",
            "name": "pe-de-roma",
            "description": "Monitors for the bonsai",
            "actions": [
                {
                    "expression": "var('my_var') == 1",
                    "code": "send_sensor_measure"
                }
            ]
        }

        serializer = serializers.DeviceRegisterSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data
