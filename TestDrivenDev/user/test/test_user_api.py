from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


CREATE_USER_URL = reverse('user:account-list')

def create_user(**payload):
    user = get_user_model().objects.create_user(**payload)
    return user


class PublicUserApiTest(TestCase):
    """Test user api(public)"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload"""
        payload = {'email':'ahashik@gasd.com','password':'testtest123445'}

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('pssword',response.data)
    
    def test_user_exist(self):
        """Create a user already exists fails"""
        payload = {'email':'demo@a.com','password':'ashikashikashik'}
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        """Test that password mush be 8 characters or bigger"""
        payload = {'email':'demo2@a.com','password':'ash'}
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()

        self.assertFalse(user_exists)   #assuring that user is not created with small password

    def test_password_8_ch_password(self):
        """creating user account with 8 character password""" 
        payload = {'email': 'demo@a.com', 'password': 'ashikash'}
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        
    def test_password_with_bigger_ch_password(self):
        """bigger password"""
        payload = {'email': 'demo@a.com', 'password': '%d%%fds    fs%%%^^^^&    &dfd   __====___       kk&'}
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
