import pytest

# from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

# from rest_framework.test import APIClient

ME_URL = reverse("user:me")

pytestmark = pytest.mark.django_db


def test_retrieve_profile_succlientcess(authenticated_user):
    user, client = authenticated_user
    """Test retrieving profile for logged in user"""
    res = client.get(ME_URL)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == {
        "name": user.name,
        "email": user.email,
    }


def test_post_me_not_allowed(authenticated_user):
    """Test that POST is not allowed on the me URL"""
    _, client = authenticated_user
    res = client.post(ME_URL, {})

    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_update_user_profile(authenticated_user):
    """Test updating the user profile for authenticated user"""
    user, client = authenticated_user
    payload = {"name": "new name", "password": "newpassword123"}

    res = client.patch(ME_URL, payload)

    user.refresh_from_db()
    assert user.name == payload["name"]
    assert user.check_password(payload["password"])
    assert res.status_code == status.HTTP_200_OK
