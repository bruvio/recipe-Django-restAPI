import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")

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


def test_create_token_for_user(client):
    """Test that a token is created for the user"""
    payload = {"email": "test@londonappdev.com", "password": "testpass"}
    create_user(**payload)
    res = client.post(TOKEN_URL, payload)

    assert "token" in res.data
    assert res.status_code == status.HTTP_200_OK


def test_create_token_invalid_credentials(client):
    """Test that token is not created if invalid credentials are given"""
    create_user(email="test@londonappdev.com", password="testpass")
    payload = {"email": "test@londonappdev.com", "password": "wrong"}
    res = client.post(TOKEN_URL, payload)

    assert "token" not in res.data
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_create_token_no_user(client):
    """Test that token is not created if user doens't exist"""
    payload = {"email": "test@londonappdev.com", "password": "testpass"}
    res = client.post(TOKEN_URL, payload)

    assert "token" not in res.data
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_create_token_missing_field(client):
    """Test that email and password are required"""
    res = client.post(TOKEN_URL, {"email": "one", "password": ""})
    assert "token" not in res.data
    assert res.status_code == status.HTTP_400_BAD_REQUEST
