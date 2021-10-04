import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def creating_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


@pytest.fixture
def authenticated_user():
    user = creating_user(
        email="test@test.com",
        password="testpass",
        name="fname",
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return user, client
