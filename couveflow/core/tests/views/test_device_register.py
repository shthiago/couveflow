from typing import Dict

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from couveflow.core.constants import INTERACTION_REGISTER_DEVICE
from couveflow.core.models import Action, Device, Interaction, Variable
from couveflow.core.tests.factories import VariableFactory


@pytest.mark.django_db
class TestDeviceRegisterViewSet:
    @pytest.fixture
    def variable(self):
        return VariableFactory(name='my_var', value=1)

    @pytest.fixture
    def data(self, variable: Variable):
        return {
            'declared_id': 'awesome-device',
            'name': 'pe-de-roma',
            'description': 'Monitors for the bonsai',
            'actions': [
                {
                    'expression': f'var(\'{variable.name}\') == 1',
                    'code': 'send_sensor_measure'
                }
            ],
        }

    @pytest.fixture
    def url(self):
        return reverse('devices-register-list')

    def test_create_device(self, url: str, auth_client: APIClient, data: Dict, user_token: Token):
        res = auth_client.post(url, data=data, format='json')

        assert res.status_code == status.HTTP_201_CREATED

        assert Device.objects.count() == 1
        device = Device.objects.first()
        assert device.declared_id == data['declared_id']
        assert device.owner == user_token.user

        assert Action.objects.count() == 1
        action = Action.objects.first()
        assert action.expression == data['actions'][0]['expression']
        assert action.device == device

    def test_recreate_device(self, url: str, auth_client: APIClient, data: Dict):
        res = auth_client.post(url, data=data, format='json')

        assert res.status_code == status.HTTP_201_CREATED

        res = auth_client.post(url, data=data, format='json')

        assert res.status_code == status.HTTP_409_CONFLICT

        assert Device.objects.count() == 1

    def test_interaction_registered(self, url: str, auth_client: APIClient, data: Dict):
        res = auth_client.post(url, data=data, format='json')

        assert res.status_code == status.HTTP_201_CREATED

        assert Interaction.objects.count() == 1
        interaction = Interaction.objects.first()
        assert interaction.type == INTERACTION_REGISTER_DEVICE

    def test_interaction_unauthorized(self, url: str, client: APIClient, data: Dict):
        res = client.post(url, data=data, format='json')

        assert res.status_code == status.HTTP_401_UNAUTHORIZED
