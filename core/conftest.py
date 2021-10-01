import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def admin_user(client) -> None:
    admin_user = get_user_model().objects.create_superuser(
        email="admin@recipes.com", password="password123"
    )
    return admin_user


@pytest.fixture
def logged_user(client, admin_user) -> None:
    client.force_login(admin_user)
    user = get_user_model().objects.create_user(
        email="test@recipes.com", password="password123", name="Test user full name"
    )
    return user
