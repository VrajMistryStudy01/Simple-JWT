from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class AuthTestCase(APITestCase):

    def setUp(self):
        """Create a test user before each test"""
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="password123"
        )
        self.login_url = "/api/login/"  # Adjusted URL for login
        self.register_url = "/api/register/"  # Adjusted URL for registration

    def test_user_login_success(self):
        """Test login with valid credentials"""
        data = {
            "email": self.user.email,
            "password": "password123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertEqual(response.data["email"], data["email"])

    def test_user_login_failure(self):
        """Test login with invalid credentials"""
        data = {
            "email": "wrong@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_user_registration(self):
        """Test user registration"""
        data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "newpassword123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])