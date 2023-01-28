from typing import Callable

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from couveflow.core.constants import INTERACTION_ASK_ACTION
from couveflow.core.models import Action, Device, Interaction, Variable
from couveflow.core.tests.factories import (ActionFactory, DeviceFactory,
                                            VariableFactory)


@pytest.mark.django_db
class TestActionsViewSet:
    @pytest.fixture
    def variable(self):
        return VariableFactory(name='my_var', value=1)

    @pytest.fixture
    def device(self, user_token: Token):
        return DeviceFactory(owner=user_token.user)

    @pytest.fixture
    def action(self, device: Device, variable: Variable):
        return ActionFactory(
            device=device,
            expression=f"var('{variable.name}') == 1",
            code='send_sensor_measure',
        )

    @pytest.fixture
    def get_url(self):
        def wrapped(declared_id: str):
            return reverse('devices-actions-ask', args=(declared_id,))
        return wrapped

    def test_ask_action(
        self,
        get_url: Callable,
        auth_client: APIClient,
        device: Device,
        action: Action,
    ):
        url = get_url(device.declared_id)
        res = auth_client.get(url)

        assert res.status_code == status.HTTP_200_OK

        data = res.json()

        assert len(data) == 1
        assert data[0]['action'] == action.code

    def test_ask_action_interaction(
            self,
            get_url: Callable,
            auth_client: APIClient,
            device: Device,
    ):
        url = get_url(device.declared_id)
        res = auth_client.get(url)

        assert res.status_code == status.HTTP_200_OK

        assert Interaction.objects.count() == 1
        interaction = Interaction.objects.first()
        assert interaction.device.declared_id == device.declared_id
        assert interaction.type == INTERACTION_ASK_ACTION

    def test_ask_action_unexistent_device(self, get_url: Callable, auth_client: APIClient):
        url = get_url('pizza')
        res = auth_client.get(url)

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_ask_action_unauthorized(self, get_url: Callable, client: APIClient, device: Device):
        url = get_url(device.declared_id)
        res = client.get(url)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED
