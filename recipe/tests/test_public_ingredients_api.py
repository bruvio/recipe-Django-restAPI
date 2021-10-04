from django.urls import reverse
from rest_framework import status

INGREDIENTS_URL = reverse("recipe:ingredient-list")


def test_login_required(client):
    """Test that login required for retrieving tags"""
    res = client.get(INGREDIENTS_URL)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
