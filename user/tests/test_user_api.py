import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

CREATE_USER_URL = reverse("user:create")

pytestmark = pytest.mark.django_db


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


def test_create_user_success(client):
    """Test creating using with a valid payload is successful"""
    payload = {
        "email": "test@test.com",
        "password": "testpass",
        "name": "name",
    }
    res = client.post(CREATE_USER_URL, payload)

    assert res.status_code == status.HTTP_201_CREATED
    user = get_user_model().objects.get(**res.data)
    assert user.check_password(payload["password"])
    assert "password" not in res.data


def test_user_exists(client):
    """Test creating a user that already exists fails"""
    payload = {
        "email": "test@test.com",
        "password": "pw",
        "name": "name",
    }
    create_user(**payload)
    res = client.post(CREATE_USER_URL, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_password_too_short(client):
    """Test that password must be more than 5 characters"""
    payload = {
        "email": "test@test.com",
        "password": "pw",
        "name": "name",
    }
    res = client.post(CREATE_USER_URL, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
    user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
    assert not user_exists
