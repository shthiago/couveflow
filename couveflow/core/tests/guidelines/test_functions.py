from typing import List

import pytest

from couveflow.core.models import Device, Interaction, Measure
from couveflow.core.tests.factories import DeviceFactory, InteractionFactory, MeasureFactory
from couveflow.core.guidelines import functions


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
    def measures(self, device: Device):
        return [
            MeasureFactory(
                device=device,
                created='2022-12-01 22:00:00',
                value=0,
                source_label="my_sensor"
            ),
            MeasureFactory(
                device=device,
                created='2022-12-01 22:35:00',
                value=12,
                source_label="my_sensor"
            ),
            MeasureFactory(
                device=device,
                created='2022-12-05 22:00:00',
                value=42,
                source_label="my_sensor"
            ),
            MeasureFactory(
                device=device,
                created='2023-12-05 22:00:00',
                value=84,
                source_label="another_sensor"
            ),
        ]

    def test_get_last_measure_for(self, device: Device, measures: List[Measure]):
        last_measure = measures[-2]
        measure_value = functions.last_measure_for(
            declared_id=device.declared_id,
            source_label="my_sensor"
        )

        assert measure_value == last_measure.value

    def test_get_last_measure_for_none(self, device: Device):
        measure_value = functions.last_measure_for(
            declared_id=device.declared_id,
            source_label="my_sensor"
        )

        assert measure_value is None
