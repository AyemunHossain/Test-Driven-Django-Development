from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


TOKEN_URL = reverse('user:token')


def create_user(**payload):
    user = get_user_model().objects.create_user(**payload)
    return user
    
class PublicUserApiTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """test that a token is created for the user"""
        payload = {'email':'test123@asd.com','password':'ashikashikashik'}
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)
        self.assertIn('token',response.data)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@londonappdev.com', password='testpass')
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        response = self.client.post(
            TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
