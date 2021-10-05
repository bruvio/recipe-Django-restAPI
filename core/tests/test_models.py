from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model

from core import models

pytestmark = pytest.mark.django_db


def sample_user(email="test@test.com", password="password"):
    return get_user_model().objects.create_user(email, password)


def test_create_user_with_email_success() -> None:
    form_data = {
        "email": "email@email.com",
        "password": "mytestpassword",
    }
    user = get_user_model().objects.create_user(**form_data)

    assert user.email == form_data["email"]
    assert user.check_password(form_data["password"])


def test_new_user_normalize() -> None:
    email = "test@EMAIL.COM"
    user = get_user_model().objects.create_user(email, "password")
    assert user.email == email.lower()


def test_new_user_invalid_email() -> None:
    with pytest.raises(ValueError):
        get_user_model().objects.create_user(None, "password")


def test_new_superuser() -> None:
    """Test creating a new superuser"""
    user = get_user_model().objects.create_superuser("email@email.com", "test123")

    assert user.is_superuser
    assert user.is_staff


def test_tag_str():
    """Test the tag string representation"""
    tag = models.Tag.objects.create(user=sample_user(), name="Vegan")

    assert str(tag) == tag.name


def test_ingredient_str():
    """Test the ingredient string representation"""
    ingredient = models.Ingredient.objects.create(user=sample_user(), name="Fennel")

    assert str(ingredient) == ingredient.name


def test_recipe_str():
    """Test the recipe string representation"""
    recipe = models.Recipe.objects.create(
        user=sample_user(), title="pizza", time_minutes=240, price=10.0
    )

    assert str(recipe) == recipe.title


@patch("uuid.uuid4")
def test_recipe_file_name_uuid(mock_uuid):
    """Test that image is saved in the correct location"""
    uuid = "test-uuid"
    mock_uuid.return_value = uuid
    file_path = models.recipe_image_file_path(None, "myimage.jpg")
    exp_path = f"uploads/recipe/{uuid}.jpg"

    assert file_path == exp_path
