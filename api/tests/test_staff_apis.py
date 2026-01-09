from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Staff
from django.contrib.auth.models import Permission


# All the tests here test individual staff permission not group permission
class AuthTests(APITestCase):
    def setUp(self):
        self.token_url = reverse("token_obtain_pair")
        self.protect_create_staff_view = reverse("create_staff")  # Ensure this name is correctly mapped in your URLs
        

        # Create a superuser with full permissions
        self.admin_staff = Staff.objects.create_user(
            username="Admin",
            email="admin@email.com",
            password="adminpass123",
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

        # Assign relevant permissions (in case is_superuser is False in future tests)
        permissions = Permission.objects.filter(
            codename__in=["staff_full_access", "add_user", "change_user", "delete_user", "view_user"]
        )
        self.admin_staff.user_permissions.set(permissions)

        # Get JWT access token for admin
        token_response = self.client.post(self.token_url, {
            "username": "admin",
            "password": "adminpass123"
        })
        self.access_token = token_response.data["access"]


        """
            Create an Ordinary Staff
        """
        regular_user = Staff.objects.create_user(
                username="Regular",
                email="regular@email.com",
                password="userpass123",
                is_active=True,
                is_staff=True  # Marked as staff, but no specific permissions
            )

            # Authenticate as the regular user
        token_response = self.client.post(self.token_url, {
                "username": "regular",
                "password": "userpass123"
            })
        self.regular_token = token_response.data["access"]

    # Create user while authenticate with superuser to test create url
    def test_create_staff_with_superuser_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(self.protect_create_staff_view, {
            "username": "Thimmy",
            "password": "Uydnv1$1",
            "email": "oluwatimileyin@gmail.com" # email has been made compulsory at staff creation
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_create_staff_without_superuser_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_token}")
        response = self.client.post(self.protect_create_staff_view, {
            "username": "Thimmy",
            "password": "1234qwer",
            "email": "oluwatimileyin962@gmail.com"
        })
        self.assertEqual(response.status_code, 403)