from typing import List

import pytest

from couveflow.core.models import Device
from couveflow.core.tests.factories import (DeviceFactory, MeasureFactory,
                                            SensorFactory)
from couveflow.graphql.schema import schema
from couveflow.tests.factories import UserFactory


@pytest.mark.django_db
class TestGraphQLSchema:
    @pytest.fixture
    def devices(self, device_1: Device, device_2: Device) -> List[Device]:
        return [
            device_1,
            device_2
        ]

    @pytest.fixture
    def device_1(self) -> Device:
        return DeviceFactory(
            declared_id="device_1",
            name="device one",
            owner=UserFactory(first_name="john", last_name="doe")
        )

    @pytest.fixture
    def device_2(self) -> Device:
        return DeviceFactory(
            declared_id="device_2",
            name="device two",
            owner=UserFactory(first_name="mary", last_name="jane")
        )

    @pytest.fixture
    def device_1_sensors_and_measures(self, device_1: Device):
        sensor1 = SensorFactory(label='sensor1', device=device_1)
        sensor2 = SensorFactory(label='sensor2', device=device_1)
        MeasureFactory(
            sensor=sensor1,
            value=500,
        )
        MeasureFactory(
            sensor=sensor2,
            value=350,
        )
        MeasureFactory(
            sensor=sensor2,
            value=350,
        )

    def test_fetch_devices(self, devices: List[Device]):
        query = '{devices { id declaredId name}}'
        result = schema.execute(query)

        assert len(result.data['devices']) == len(devices)

    @pytest.mark.usefixtures('device_1_sensors_and_measures', 'devices')
    def test_fetch_devices_filter_device(self):
        query = '''
            {
                devices (declaredId: "device_1"){
                    id
                    declaredId
                    name
                    sensors {
                        label
                    }
                }
            }
        '''
        result = schema.execute(query)

        assert len(result.data['devices']) == 1
        ret_device_1 = result.data['devices'][0]

        expected_sensors = [
            {'label': 'sensor1'},
            {'label': 'sensor2'},
        ]

        assert ret_device_1['sensors'] == expected_sensors

    @pytest.mark.usefixtures('device_1_sensors_and_measures', 'devices')
    def test_fetch_devices_filter_device_and_sensor(self):
        query = '''
            {
                devices (declaredId: "device_1"){
                    id
                    declaredId
                    name
                    sensors (label: "sensor1") {
                        label
                    }
                }
            }
        '''
        result = schema.execute(query)

        assert len(result.data['devices']) == 1
        ret_device_1 = result.data['devices'][0]

        expected_sensors = [
            {'label': 'sensor1'},
        ]

        assert ret_device_1['sensors'] == expected_sensors

    @pytest.mark.usefixtures('device_1_sensors_and_measures', 'devices')
    def test_fetch_devices_filter_device_and_sensor_with_measures(self):
        query = '''
            {
                devices (declaredId: "device_1"){
                    id
                    declaredId
                    name
                    sensors (label: "sensor1") {
                        label
                        measures { value }
                    }
                }
            }
        '''
        result = schema.execute(query)

        assert len(result.data['devices']) == 1
        ret_device_1 = result.data['devices'][0]

        expected_sensors = [
            {
                'label': 'sensor1',
                'measures': [{'value': '500.00'}],
            },
        ]

        assert ret_device_1['sensors'] == expected_sensors
