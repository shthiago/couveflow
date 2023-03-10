from typing import List

import pytest

from couveflow.core.guidelines import functions
from couveflow.core.models import Device, Interaction, Measure, Sensor
from couveflow.core.tests.factories import (DeviceFactory, InteractionFactory,
                                            MeasureFactory, SensorFactory)


@pytest.mark.django_db
class TestLastInteractionTimestamp:
    @pytest.fixture
    def device(self):
        return DeviceFactory()

    @pytest.fixture
    def interactions(self, device: Device):
        return [
            InteractionFactory(device=device, created='2022-12-01 22:00:00'),
            InteractionFactory(device=device, created='2022-12-01 22:35:00'),
            InteractionFactory(device=device, created='2022-12-05 22:00:00'),
        ]

    def test_get_last_interaction_timestamp(self, device: Device, interactions: List[Interaction]):
        last_interaction = interactions[-1]
        last_interaction_ts = functions.last_interaction_timestamp(
            declared_id=device.declared_id)

        assert last_interaction_ts == last_interaction.created

    def test_get_last_interaction_timestamp_none(self, device: Device):
        last_interaction_ts = functions.last_interaction_timestamp(
            declared_id=device.declared_id)

        assert last_interaction_ts is None


@pytest.mark.django_db
class TestLastMeasureFor:
    @pytest.fixture
    def device(self):
        return DeviceFactory()

    @pytest.fixture
    def sensor(self, device: Device):
        return SensorFactory(device=device)

    @pytest.fixture
    def measures(self, sensor: Device):
        other_sensor = SensorFactory(
            device=sensor.device, label='other_sensor')
        return [
            MeasureFactory(
                sensor=sensor,
                created='2022-12-01 22:00:00',
                value=0,
            ),
            MeasureFactory(
                sensor=sensor,
                created='2022-12-01 22:35:00',
                value=12,
            ),
            MeasureFactory(
                sensor=sensor,
                created='2022-12-05 22:00:00',
                value=42,
            ),
            MeasureFactory(
                sensor=other_sensor,
                created='2023-12-05 22:00:00',
                value=84,
            ),
        ]

    def test_get_last_measure_for(self, sensor: Sensor, device: Device, measures: List[Measure]):
        last_measure = measures[-2]
        measure_value = functions.last_measure_for(
            declared_id=device.declared_id,
            sensor_label=sensor.label,
        )

        assert measure_value == last_measure.value

    def test_get_last_measure_for_none(self, sensor: Sensor, device: Device):
        measure_value = functions.last_measure_for(
            declared_id=device.declared_id,
            sensor_label=sensor.label,
        )

        assert measure_value is None
