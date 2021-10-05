import os
import tempfile

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from PIL import Image
from rest_framework import status

from core.models import Ingredient, Recipe, Tag
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer

RECIPES_URL = reverse("recipe:recipe-list")
pytestmark = pytest.mark.django_db


def image_upload_url(recipe_id):
    """return url for recipe image upload

    :param recipe_id: [description]
    :type recipe_id: [type]
    """
    return reverse("recipe:recipe-upload-image", args=recipe_id)


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        "title": "Sample recipe",
        "time_minutes": 10,
        "price": 5.00,
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


def sample_tag(user, name="Main course"):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name="Salt"):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse("recipe:recipe-detail", args=[recipe_id])


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


def test_view_recipe_detail(authenticated_user):

    """Test viewing a recipe detail"""
    user, client = authenticated_user
    recipe = sample_recipe(user=user)
    recipe.tags.add(sample_tag(user=user))
    recipe.ingredients.add(sample_ingredient(user=user))

    url = detail_url(recipe.id)
    res = client.get(url)

    serializer = RecipeDetailSerializer(recipe)
    assert res.data == serializer.data


def test_create_recipe(authenticated_user):
    """testing create recipe

    :param authenticated_user: [description]
    :type authenticated_user: [type]
    """
    _, client = authenticated_user
    payload = {"title": "pizze", "time_minutes": 30, "price": 20}
    res = client.post(RECIPES_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    recipe = Recipe.objects.get(id=res.data["id"])
    for key in payload.keys():
        assert payload[key] == getattr(recipe, key)


def test_create_recipe_with_tags(authenticated_user):
    """testing create recipe with tag

    :param authenticated_user: [description]
    :type authenticated_user: [type]
    """
    user, client = authenticated_user
    tag1 = sample_tag(user=user, name="main")
    tag2 = sample_tag(user=user, name="lallero")

    payload = {
        "title": "newrecipe",
        "tags": [tag1.id, tag2.id],
        "time_minutes": 12,
        "price": 123.00,
    }

    res = client.post(RECIPES_URL, payload)

    assert res.status_code == status.HTTP_201_CREATED
    recipe = Recipe.objects.get(id=res.data["id"])
    tags = recipe.tags.all()
    assert tags.count() == 2
    assert tag1 in tags
    assert tag2 in tags


def test_create_recipe_with_ingredient(authenticated_user):
    """testing create recipe with ingredient

    :param authenticated_user: [description]
    :type authenticated_user: [type]
    """
    user, client = authenticated_user
    ingredient1 = sample_ingredient(user=user, name="salt")
    ingredient2 = sample_ingredient(user=user, name="red salt")

    payload = {
        "title": "newrecipe",
        "ingredients": [ingredient1.id, ingredient2.id],
        "time_minutes": 12,
        "price": 123.00,
    }

    res = client.post(RECIPES_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    recipe = Recipe.objects.get(id=res.data["id"])
    ingredients = recipe.ingredients.all()
    assert ingredients.count() == 2
    assert ingredient1 in ingredients
    assert ingredient2 in ingredients


def test_partial_update_recipe(authenticated_user):
    """Test updating a recipe with patch"""
    user, client = authenticated_user
    recipe = sample_recipe(user=user)
    recipe.tags.add(sample_tag(user=user))
    new_tag = sample_tag(user=user, name="Curry")

    payload = {"title": "Chicken tikka", "tags": [new_tag.id]}
    url = detail_url(recipe.id)
    client.patch(url, payload)

    recipe.refresh_from_db()
    assert recipe.title == payload["title"]
    tags = recipe.tags.all()
    assert len(tags) == 1
    assert new_tag in tags


def test_full_update_recipe(authenticated_user):
    """Test updating a recipe with put"""
    user, client = authenticated_user
    recipe = sample_recipe(user=user)
    recipe.tags.add(sample_tag(user=user))

    payload = {"title": "Spaghetti carbonara", "time_minutes": 25, "price": 5.00}
    url = detail_url(recipe.id)
    client.put(url, payload)

    recipe.refresh_from_db()
    assert recipe.title == payload["title"]
    assert recipe.time_minutes == payload["time_minutes"]
    assert recipe.price == payload["price"]
    tags = recipe.tags.all()
    assert len(tags) == 0


def test_image_upload(authenticated_user):
    user, client = authenticated_user
    recipe = sample_recipe(user=user)
    url = image_upload_url(recipe.id)
    with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
        img = Image.new("RGB", (10, 10))
        img.save(ntf, format="JPEG")
        ntf.seek(0)
        res = client.post(url, {"image": ntf}, format="multipart")

    recipe.refresh_from_db()
    assert res.status_code == status.HTTP_200_OK
    assert "image" in res.data
    assert os.path.exists(recipe.image.path)
    recipe.image.delete()


def test_upload_image_bad_request(authenticated_user):
    """Test uploading an invalid image"""
    user, client = authenticated_user
    recipe = sample_recipe(user=user)
    url = image_upload_url(recipe.id)
    res = client.post(url, {"image": "notimage"}, format="multipart")

    assert res.status_code, status.HTTP_400_BAD_REQUEST
    recipe.image.delete()
