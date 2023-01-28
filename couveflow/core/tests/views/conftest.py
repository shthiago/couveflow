import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from couveflow.tests.factories import TokenFactory


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_token():
    return TokenFactory()


@pytest.fixture
def auth_client(client: APIClient, user_token: Token):
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    return client
