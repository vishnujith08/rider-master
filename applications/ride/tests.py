from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from rest_framework.test import APIClient
from rest_framework import status

from .models import Ride, RideRequest
from applications.api.serializers import RideSerializer, RideRequestSerializer, DriverLocationSerializer, \
    UserListingSerializer
from applications.accounts.models import User, DriverLocation


# tests for ride models
class RideModelTest(TestCase):
    def setUp(self):
        self.rider = User.objects.create_user(
            username="rider",
            password="riderpassword",
        )
        self.driver = User.objects.create_user(
            username="driver",
            password="driverpassword",
        )

    def test_ride_creation(self):
        ride = Ride.objects.create(
            rider=self.rider,
            driver=self.driver,
            pickup_loc_latitude="12.34",
            pickup_loc_longitude="56.78",
            dropoff_loc_latitude="34.56",
            dropoff_loc_logitude="78.12",
            status="pending",
        )
        self.assertEqual(ride.rider, self.rider)
        self.assertEqual(ride.driver, self.driver)
        self.assertEqual(ride.status, "pending")

    def test_ride_string_representation(self):
        ride = Ride.objects.create(rider=self.rider, status="pending")
        self.assertEqual(str(ride), "rider")


class RideRequestModelTest(TestCase):
    def setUp(self):
        self.rider = User.objects.create_user(
            username="rider",
            password="riderpassword",
        )
        self.driver = User.objects.create_user(
            username="driver",
            password="driverpassword",
        )
        self.ride = Ride.objects.create(
            rider=self.rider,
            driver=self.driver,
            pickup_loc_latitude="12.34",
            pickup_loc_longitude="56.78",
            dropoff_loc_latitude="34.56",
            dropoff_loc_logitude="78.12",
            status="pending",
        )

    def test_ride_request_creation(self):
        ride_request = RideRequest.objects.create(
            driver=self.driver,
            ride=self.ride,
            status="pending",
        )
        self.assertEqual(ride_request.driver, self.driver)
        self.assertEqual(ride_request.ride, self.ride)
        self.assertEqual(ride_request.status, "pending")

    def test_ride_request_string_representation(self):
        ride_request = RideRequest.objects.create(driver=self.driver, ride=self.ride, status="pending")
        self.assertEqual(str(ride_request), "rider")


# tests for ride apis
User = get_user_model()


class RideViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.rider = User.objects.create_user(
            username="rider@gmail.com",
            password="riderpassword",
        )
        self.client.force_authenticate(user=self.rider)

    def test_create_ride(self):
        url = '/api/ride/'
        data = {
            "rider": self.rider.id,
            "pickup_loc_latitude": 12.34,
            "pickup_loc_longitude": 56.78,
            "dropoff_loc_latitude": 34.56,
            "dropoff_loc_logitude": 78.12,
            "status": "pending",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_rides(self):
        url = '/api/ride/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RideRequestViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.rider = User.objects.create_user(
            username="rider",
            password="riderpassword",
        )
        self.driver = User.objects.create_user(
            username="driver",
            password="driverpassword",
        )
        self.client.force_authenticate(user=self.rider)

    def test_create_ride_request(self):
        url = '/api/ride-request/'
        ride = Ride.objects.create(rider=self.rider, status="pending")
        data = {
            "ride": ride.id,
            "status": "pending",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_ride_request(self):
        ride = Ride.objects.create(rider=self.rider, status="pending")
        ride_request = RideRequest.objects.create(ride=ride, status="pending")
        url = f'/api/ride-request/{ride_request.id}/'
        data = {
            "status": "success",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DriverLocationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.driver = User.objects.create_user(
            username="driver",
            password="driverpassword",
            user_role="driver"
        )
        self.client.force_authenticate(user=self.driver)
        self.location = DriverLocation.objects.create(location=Point(12.34, 56.78), is_driver_available=True)

    def test_create_driver_location(self):
        url = '/api/driver-location/'
        data = {
            "latitude": 12.34,
            "longitude": 56.78,
            "is_driver_available": True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_driver_location(self):
        location_id = self.location.id
        url = f'/api/driver-location/{location_id}/'
        data = {
            "latitude": 12.35,
            "longitude": 56.79,
            "is_driver_available": False,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DriversListingViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.rider = User.objects.create_user(
            username="rider",
            password="riderpassword",
        )
        self.client.force_authenticate(user=self.rider)

    def test_list_available_drivers(self):
        url = '/api/driver-listing/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

