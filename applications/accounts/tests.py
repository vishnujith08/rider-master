from django.test import TestCase
from django.contrib.gis.geos import Point
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import User, DriverLocation


# tests for user model
class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            full_name="Test User",
            phone="+1234567890",
            user_role="driver"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.full_name, "Test User")
        self.assertEqual(str(user), "testuser")


class DriverLocationModelTest(TestCase):
    def test_driver_location_creation(self):
        point = Point(x=1.23, y=4.56)
        driver_location = DriverLocation.objects.create(
            location=point,
            is_driver_available=True
        )
        self.assertEqual(driver_location.location, point)
        self.assertEqual(str(driver_location), "1.23, 4.56")


# API tests
# class LoginViewTest(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser",
#             password="testpassword",
#         )
#
#     def test_login_success(self):
#         url = '/api/login/'
#         data = {
#             "email": "testuser",
#             "password": "testpassword",
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_login_failure(self):
#         url = '/api/login/'
#         data = {
#             "email": "testuser",
#             "password": "wrongpassword",
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginViewTest(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser@example.com', password='testpassword', email='testuser@example.com')

    def test_login_success(self):
        url = '/api/login/'
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['status'], 'success')

    def test_login_failure(self):
        url = '/api/login/'
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Invalid credentials')

    def test_login_user_not_registered(self):
        url = '/api/login/'
        data = {
            'email': 'nonexistent@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ["User not registered"])


class ProfileCreateViewTest(APITestCase):
    def test_profile_creation(self):
        url = '/api/profile-create/'
        data = {
            "username": "newuser@gmail.com",
            "password": "newpassword",
            "full_name": "New User",
            "phone": "+917654321099",
            "user_role": "rider",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
