from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AuthTestCase(APITestCase):

    def setUp(self):
        """Create a test user before each test"""
        self.user = User.objects.create_user(email="test@example.com", username="testuser", password="password123")
        self.login_url = "/api/token/"

    def test_user_registration(self):
        """Test user registration"""
        data = {"email": "newuser@example.com", "username": "newuser", "password": "newpassword123"}
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])

    def test_user_login(self):
        """Test user login and token retrieval"""
        data = {"email": "test@example.com", "password": "password123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        """Test refreshing JWT token"""
        refresh = str(RefreshToken.for_user(self.user))
        response = self.client.post("/api/token/refresh/", {"refresh": refresh})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_get_user_profile(self):
        """Test retrieving user profile"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/user/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_change_password(self):
        """Test changing user password"""
        self.client.force_authenticate(user=self.user)
        data = {"old_password": "password123", "new_password": "newsecurepassword"}
        response = self.client.post("/api/password-change/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password updated successfully.") 
