from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import User
from django.contrib.auth.models import Permission


class AuthTests(APITestCase):
    def setUp(self):
        self.token_url = reverse("token_obtain_pair")
        self.protected_url = reverse("list_create_user")  # Ensure this name is correctly mapped in your URLs
        self.protected_create_user_url = reverse("list_create_user")

        # Create a superuser with full permissions
        self.admin_user = User.objects.create_user(
            username="Admin",
            email="admin@email.com",
            password="adminpass123",
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        # Assign relevant permissions (in case is_superuser is False in future tests)
        permissions = Permission.objects.filter(
            codename__in=["can_manage_user", "add_user", "change_user", "delete_user", "view_user"]
        )
        self.admin_user.user_permissions.set(permissions)

        # Get JWT access token for admin
        token_response = self.client.post(self.token_url, {
            "username": "Admin",
            "password": "adminpass123"
        })
        self.access_token = token_response.data["access"]


        """
            Create an Ordinary User
        """
        regular_user = User.objects.create_user(
                username="Regular",
                email="regular@email.com",
                password="userpass123",
                is_active=True,
                is_staff=True  # Marked as staff, but no specific permissions
            )

            # Authenticate as the regular user
        token_response = self.client.post(self.token_url, {
                "username": "Regular",
                "password": "userpass123"
            })
        self.regular_token = token_response.data["access"]


    def test_authenticated_access_to_protected_view(self):
        """Ensure authenticated user with proper permissions can access the view."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_unauthenticated_access_is_denied(self):
        """Ensure access is denied when no credentials are provided."""
        self.client.credentials()  # Clears any previous credentials
        response = self.client.get(self.protected_url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])


    def test_user_without_permission_is_denied(self):
        """Ensure that a staff user without the required permissions is denied access."""

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_token}")
        response = self.client.get(self.protected_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # Authenticate with superuser to test create url
    def test_create_user_with_superuser_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(self.protected_create_user_url, {
            "username": "Thimmy",
            "password": "1234qwer",
            "email": ""
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_without_superuser_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_token}")
        response = self.client.post(self.protected_create_user_url, {
            "username": "Thimmy",
            "password": "1234qwer",
            "email": ""
        })
        self.assertIn(response.status_code, [401, 403])

    def test_list_users_with_superuser_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.protected_create_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_list_users_without_superuser_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_token}")
        response = self.client.get(self.protected_create_user_url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)