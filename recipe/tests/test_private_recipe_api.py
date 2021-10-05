import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse("recipe:recipe-list")
pytestmark = pytest.mark.django_db


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        "title": "Sample recipe",
        "time_minutes": 10,
        "price": 5.00,
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


def test_retrieve_recipes(authenticated_user):
    """Test retrieving list of recipes"""
    user, client = authenticated_user
    sample_recipe(user=user)
    sample_recipe(user=user, price=2)

    res = client.get(RECIPES_URL)

    recipes = Recipe.objects.all().order_by("-id")
    serializer = RecipeSerializer(recipes, many=True)
    assert res.status_code == status.HTTP_200_OK

    assert res.data == serializer.data


def test_recipes_limited_to_user(authenticated_user):
    user, client = authenticated_user
    """Test retrieving recipes for user"""
    user2 = get_user_model().objects.create_user("other@test.com", "password123")
    sample_recipe(user=user2)
    sample_recipe(user=user)

    res = client.get(RECIPES_URL)

    recipes = Recipe.objects.filter(user=user)
    serializer = RecipeSerializer(recipes, many=True)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data == serializer.data
