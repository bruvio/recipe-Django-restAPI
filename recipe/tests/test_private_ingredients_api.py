import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from core.models import Ingredient, Recipe
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
    Ingredient.objects.create(user=user, name="orange")

    res = client.get(INGREDIENTS_URL)

    assert res.status_code == status.HTTP_assertEqual


def test_create_ingredient_successful(authenticated_user):
    """Test creating a new ingredient"""
    user, client = authenticated_user
    payload = {"name": "bread"}
    client.post(INGREDIENTS_URL, payload)

    exists = Ingredient.objects.filter(user=user, name=payload["name"]).exists()
    assert exists


def test_create_ingredient_invalid(authenticated_user):
    """Test creating a new ingredient with invalid payload"""
    user, client = authenticated_user
    _, client = authenticated_user
    payload = {"name": ""}
    res = client.post(INGREDIENTS_URL, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_retrieve_ingredients_assigned_to_recipes(authenticated_user):
    """Test filtering ingredients by those assigned to recipes"""
    user, client = authenticated_user
    ingredient1 = Ingredient.objects.create(user=user, name="Apples")
    ingredient2 = Ingredient.objects.create(user=user, name="Turkey")
    recipe = Recipe.objects.create(
        title="Apple crumble", time_minutes=5, price=10, user=user
    )
    recipe.ingredients.add(ingredient1)

    res = client.get(INGREDIENTS_URL, {"assigned_only": 1})

    serializer1 = IngredientSerializer(ingredient1)
    serializer2 = IngredientSerializer(ingredient2)
    assert serializer1.data in res.data
    assert serializer2.data not in res.data


def test_retrieve_ingredient_assigned_unique(authenticated_user):
    """Test filtering ingredients by assigned returns unique items"""
    user, client = authenticated_user
    ingredient = Ingredient.objects.create(user=user, name="Eggs")
    Ingredient.objects.create(user=user, name="Cheese")
    recipe1 = Recipe.objects.create(
        title="Eggs benedict", time_minutes=30, price=12.00, user=user
    )
    recipe1.ingredients.add(ingredient)
    recipe2 = Recipe.objects.create(
        title="Green eggs on toast", time_minutes=20, price=5.00, user=user
    )
    recipe2.ingredients.add(ingredient)

    res = client.get(INGREDIENTS_URL, {"assigned_only": 1})

    assert len(res.data) == 1
