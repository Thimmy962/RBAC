from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import User  # your custom user model

class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')  # your actual view name
        self.token_url = reverse('token_obtain_pair')

        self.user_data = {
            "username": "john",
            "email": "JohnDoe@Email.Com",
            "password": "securepass123"
        }

        # Register the user
        self.client.post(self.register_url, self.user_data)

    def test_user_is_saved_with_cleaned_data(self):
        user = User.objects.first()
        self.assertEqual(user.username, "John")  # title-cased
        self.assertEqual(user.email, "johndoe@email.com")  # lowercased

    def test_login_with_original_username_succeeds(self):
        response = self.client.post(self.token_url, {
            "username": "John",  # stored as "John"
            "password": "securepass123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_login_with_lowercase_username_succeeds(self):
        response = self.client.post(self.token_url, {
            "username": "john",  # input lowercase, gets title-cased internally
            "password": "securepass123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(self.token_url, {
            "username": "john",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 401)

    def test_login_with_nonexistent_user_fails(self):
        response = self.client.post(self.token_url, {
            "username": "nonexist",
            "password": "whatever"
        })
        self.assertEqual(response.status_code, 401)
