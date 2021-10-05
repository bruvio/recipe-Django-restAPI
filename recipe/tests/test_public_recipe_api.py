from django.urls import reverse
from rest_framework import status

RECIPES_URL = reverse("recipe:recipe-list")


def test_login_required(client):
    """Test that login required for retrieving tags"""
    res = client.get(RECIPES_URL)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
