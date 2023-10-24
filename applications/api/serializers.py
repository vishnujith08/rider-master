from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework import status
import phonenumbers
from phonenumber_field.serializerfields import PhoneNumberField

from applications.accounts.models import User, DriverLocation
from applications.ride.models import Ride, RideRequest


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        if not User.objects.filter(email__iexact=attrs['email']).exists():
            raise serializers.ValidationError("User not registered")
        return attrs


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions', ]


class RideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = '__all__'


class RideRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = RideRequest
        fields = '__all__'


class DriverLocationSerializer(serializers.ModelSerializer):
    latitude = serializers.CharField(required=False)
    longitude = serializers.CharField(required=False)

    class Meta:
        model = DriverLocation
        fields = '__all__'

