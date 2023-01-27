from typing import Callable, Dict

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from couveflow.core.constants import INTERACTION_SAVE_MEASURE
from couveflow.core.models import Device, Interaction, Measure
from couveflow.core.tests.factories import DeviceFactory


@pytest.mark.django_db
class TestActionsViewSet:
    @pytest.fixture
    def device(self):
        return DeviceFactory()

    @pytest.fixture
    def get_url(self):
        def wrapped(declared_id: str):
            return reverse('devices-measures-register', args=(declared_id,))
        return wrapped

    @pytest.fixture
    def data(self):
        return {
            'value': 12,
            'source_label': 'my_awesome_sensor',
        }

    def test_register_measure(
        self,
        get_url: Callable,
        client: APIClient,
        device: Device,
        data: Dict
    ):
        url = get_url(device.declared_id)
        res = client.post(url, data=data, format='json')

        assert res.status_code == status.HTTP_200_OK

        assert Measure.objects.count() == 1
        measure = Measure.objects.first()

        assert measure.device == device
        assert measure.value == data['value']
        assert measure.source_label == data['source_label']

    def test_register_measure_interaction(
        self,
        get_url: Callable,
        client: APIClient,
        device: Device,
        data: Dict
    ):
        url = get_url(device.declared_id)
        res = client.post(url, data=data)

        assert res.status_code == status.HTTP_200_OK

        assert Interaction.objects.count() == 1
        interaction = Interaction.objects.first()
        assert interaction.device.declared_id == device.declared_id
        assert interaction.type == INTERACTION_SAVE_MEASURE

    def test_ask_action_unexistent_device(self, get_url: Callable, client: APIClient):
        url = get_url('pizza')
        res = client.post(url)

        assert res.status_code == status.HTTP_404_NOT_FOUND