import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse("recipe:ingredient-list")
pytestmark = pytest.mark.django_db


def test_retrieve_ingredient_success(authenticated_user):
    user, client = authenticated_user
    """Test retrieving ingredient for logged in user"""
    Ingredient.objects.create(user=user, name="salt")
    Ingredient.objects.create(user=user, name="lettuce")

    res = client.get(INGREDIENTS_URL)

    ingredients = Ingredient.objects.all().order_by("-name")
    serializer = IngredientSerializer(ingredients, many=True)

    assert res.status_code == status.HTTP_200_OK

    assert res.data == serializer.data


def test_ingredients_limited_to_user(authenticated_user):
    """Test that ingredients returned are for authenticated user"""
    user, client = authenticated_user
    user2 = get_user_model().objects.create_user("other@test.com", "testpass")
    Ingredient.objects.create(user=user2, name="banana")
    ingredient = Ingredient.objects.create(user=user, name="orange")

    res = client.get(INGREDIENTS_URL)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0]["name"] == ingredient.name


def test_create_ingredient_successful(authenticated_user):
    """Test creating a new ingredient"""
    user, client = authenticated_user
    payload = {"name": "bread"}
    client.post(INGREDIENTS_URL, payload)

    exists = Ingredient.objects.filter(user=user, name=payload["name"]).exists()
    assert exists


def test_create_ingredient_invalid(authenticated_user):
    """Test creating a new ingredient with invalid payload"""
    _, client = authenticated_user
    payload = {"name": ""}
    res = client.post(INGREDIENTS_URL, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
