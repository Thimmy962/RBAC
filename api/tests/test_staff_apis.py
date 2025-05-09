from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Staff
from django.contrib.auth.models import Permission


# All the tests here test individual staff permission not group permission
class AuthTests(APITestCase):
    def setUp(self):
        self.token_url = reverse("token_obtain_pair")
        self.protect_list_create_staff_view = reverse("list_create_staff")  # Ensure this name is correctly mapped in your URLs
        

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

    def test_retrieve_staff_without_credentials(self):
        """Ensure authenticated logged with proper permissionin alone can access this view"""
        url = reverse("retrieve_update_delete_staff", kwargs = {"pk": 20})
        self.client.credentials()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 401)

    def test_retrieve_staff_with_credentials_of_regular_staff(self):
        url = reverse("retrieve_update_delete_staff", kwargs = {"pk": 20})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_token}")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)

    def test_retrieve_staff_with_credentials_of_admin_staff(self):
        url = reverse("retrieve_update_delete_staff", kwargs = {"pk": 20})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 404)

    def test_authenticated_access_to_protected_view(self):
        """Ensure authenticated staff with proper permissions can access the view."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.protect_list_create_staff_view)
        self.assertEqual(response.status_code, 200)


    def test_unauthenticated_access_is_denied(self):
        """Ensure access is denied when no credentials are provided."""
        self.client.credentials()  # Clears any previous credentials
        response = self.client.get(self.protect_list_create_staff_view)
        self.assertEqual(response.status_code, 401)


    def test_staff_without_permission_is_denied(self):
        """Ensure that a staff user without the required permissions is denied access."""

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_token}")
        response = self.client.get(self.protect_list_create_staff_view)

        self.assertEqual(response.status_code, 403)


    # Create user while authenticate with superuser to test create url
    def test_create_staff_with_superuser_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(self.protect_list_create_staff_view, {
            "username": "Thimmy",
            "password": "1234qwer",
            "email": ""
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_create_staff_without_superuser_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_token}")
        response = self.client.post(self.protect_list_create_staff_view, {
            "username": "Thimmy",
            "password": "1234qwer",
            "email": ""
        })
        self.assertEqual(response.status_code, 403)

    
    def test_list_staff_with_superuser_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.protect_list_create_staff_view)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_list_staff_without_superuser_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.regular_token}")
        response = self.client.get(self.protect_list_create_staff_view)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)


    # trying the view user api with a delete user permission. Expects Unauthorized 
    def test_user_without_request_method_apiview_for_staff_model(self):
        # create user
        user = Staff.objects.create_user(
            username="Amen",
            password="amen")
        
        # set permission to delet user
        permissions = Permission.objects.filter(
            codename__in=["delete_user"]
        )

        user.user_permissions.set(permissions)

        # login with created user
        res = self.client.post(self.token_url, {
            "username": "amen", "password": "amen"
        })
        token = res.data["access"]

        # Try accessing the list user api view
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.protect_list_create_staff_view)
        self.assertEqual(response.status_code, 403)