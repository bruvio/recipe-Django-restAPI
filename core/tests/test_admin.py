import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_users_listed(client, logged_user):
    """Test that users are listed on user page"""

    url = reverse("admin:core_user_changelist")
    res = client.get(url)
    assert logged_user.name in str(res.content)
    assert logged_user.email in str(res.content)


def test_user_page_change(client, logged_user):
    """Test that the user edit page works"""
    url = reverse("admin:core_user_change", args=[logged_user.id])
    res = client.get(url)

    assert res.status_code == 200


def test_create_user_page(client, logged_user):
    """Test that the create user page works"""
    url = reverse("admin:core_user_add")
    res = client.get(url)

    assert res.status_code == 200
