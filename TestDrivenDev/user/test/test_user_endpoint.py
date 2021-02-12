from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

USER_ME = reverse('user:me')

def create_user(**payload):
    user = get_user_model().objects.create_user(**payload)
    return user

class PrivateUserEndpoints(TestCase):

    def setUp(self):
        self.user = create_user(
            email = "testashik@ashik.com",
            password = "ashikashikashik"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_user_info_success(self):
        """Test retrive user info for logged in user"""
        response = self.client.get(USER_ME)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({'id':self.user.id,'email':self.user.email}, response.data)
    
    def test_retrive_user_info_success_2(self):
        """Test retrive user info for logged in user"""
        USER_DETAIL = reverse('user:account-detail', args=[self.user.id])
        
        response = self.client.get(USER_DETAIL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({'id':self.user.id,'email':self.user.email}, response.data)

    def test_post_not_allowed(self):
        """Test that post method is failed in USER_ME url"""
        response = self.client.post(USER_ME, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_user_info(self):
        """Test that user inof is updated successfully"""
        payload = {'email': 'ayemunhossain@gmail.com'}
        response = self.client.patch(USER_ME, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload['email'])