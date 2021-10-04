import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse("recipe:tag-list")
pytestmark = pytest.mark.django_db


def test_retrieve_tag_success(authenticated_user):
    user, client = authenticated_user
    """Test retrieving tag for logged in user"""
    Tag.objects.create(user=user, name="Vegan")
    Tag.objects.create(user=user, name="Dessert")

    res = client.get(TAGS_URL)
    print(res.status_code)

    tags = Tag.objects.all().order_by("-name")
    serializer = TagSerializer(tags, many=True)

    assert res.status_code == status.HTTP_200_OK

    assert res.data == serializer.data


def test_tags_limited_to_user(authenticated_user):
    """Test that tags returned are for authenticated user"""
    user, client = authenticated_user
    user2 = get_user_model().objects.create_user("other@test.com", "testpass")
    Tag.objects.create(user=user2, name="Fruity")
    tag = Tag.objects.create(user=user, name="Comfort Food")

    res = client.get(TAGS_URL)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0]["name"] == tag.name


def test_create_tag_successful(authenticated_user):
    """Test creating a new tag"""
    user, client = authenticated_user
    payload = {"name": "Simple"}
    client.post(TAGS_URL, payload)

    exists = Tag.objects.filter(user=user, name=payload["name"]).exists()
    assert exists


def test_create_tag_invalid(authenticated_user):
    """Test creating a new tag with invalid payload"""
    _, client = authenticated_user
    payload = {"name": ""}
    res = client.post(TAGS_URL, payload)

    assert res.status_code == status.HTTP_400_BAD_REQUEST
