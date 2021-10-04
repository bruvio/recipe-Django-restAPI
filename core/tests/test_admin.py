import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_users_listed(client, logged_user):
    """Test that users are listed on user page"""

    url = reverse("admin:core_user_changelist")
    res = client.get(url)
    print(res)
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


# from django.test import TestCase, Client
# from django.contrib.auth import get_user_model
# from django.urls import reverse


# class AdminSiteTests(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.admin_user = get_user_model().objects.create_superuser(
#             email='admin@londonappdev.com',
#             password='password123'
#         )
#         self.client.force_login(self.admin_user)
#         self.user = get_user_model().objects.create_user(
#             email='test@londonappdev.com',
#             password='password123',
#             name='Test user full name'
#         )

#     def test_users_listed(self):
#         """Test that users are listed on user page"""
#         url = reverse('admin:core_user_changelist')
#         res = self.client.get(url)
#         print(res)
#         self.assertContains(res, self.user.name)
#         self.assertContains(res, self.user.email)
