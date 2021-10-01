import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


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
