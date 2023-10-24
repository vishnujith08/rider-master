from django.contrib.auth import authenticate, login
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.serializers import ValidationError

from applications.api.serializers import LoginSerializer, UserCreateSerializer, RideSerializer, \
    RideRequestSerializer, UserListingSerializer, DriverLocationSerializer
from applications.accounts.models import User, DriverLocation
from applications.ride.models import Ride, RideRequest


class LoginView(APIView):
    """
    Views for a user to login
    @param: email:str, password:str
    @return: dict: status success:str, token:str
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        password = serializer.data['password']
        user = authenticate(username=email, password=password)
        if not user:
            return Response({'message': 'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"status": "success", "token": token.key}, status=status.HTTP_200_OK)


class ProfileCreateView(viewsets.ModelViewSet):
    """
    Views for a user to create an account-profile
    @param: profile details:str
    @return: dict:profile details:str
    """

    http_method_names = ['post', ]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        password = serializer.validated_data.get('password')
        user = serializer.save(email=serializer.validated_data['username'])
        user.set_password(password)
        user.save()


class RideView(viewsets.ModelViewSet):
    """
    Views for listing, creating ride details and status update
    @param: ride id:str
    @return: dict:ride details:str
    """

    http_method_names = ['get', 'post', 'patch', ]
    serializer_class = RideSerializer
    queryset = Ride.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)


class RideRequestView(viewsets.ModelViewSet):
    """
    Views for listing, creating ride request details and for updating driver response
    @param: ride request details:str
    @return: dict:ride request details:str
    """

    http_method_names = ['get', 'post', 'patch', ]
    serializer_class = RideRequestSerializer
    queryset = RideRequest.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        ride_id = self.request.data.get('ride')
        try:
            ride = Ride.objects.get(pk=ride_id)
        except Ride.DoesNotExist:
            raise ValidationError("Ride not found")

        # Check if the ride is related to the requesting user (rider)
        if ride.rider != self.request.user:
            raise ValidationError("This ride is not related to you")
        serializer.save(ride=ride)

    def update(self, request, *args, **kwargs):
        ride_request = self.get_object()
        driver_response = request.data.get('status', ride_request.status)
        if driver_response == 'success':
            ride_obj = ride_request.ride
            ride_obj.driver = request.user
            ride_obj.save()
        return Response({'message': 'success', 'status': status.HTTP_200_OK})


class DriverLocationView(viewsets.ModelViewSet):
    """
    Views for adding and updating driver location
    """

    http_method_names = ['get', 'post', 'patch', ]
    serializer_class = DriverLocationSerializer
    queryset = DriverLocation.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        latitude = serializer.validated_data.get('latitude')
        longitude = serializer.validated_data.get('longitude')
        is_driver_available = serializer.validated_data.get('is_driver_available', True)

        if latitude is not None and longitude is not None:
            loc = Point(float(longitude), float(latitude), srid=4326)
            location = DriverLocation(location=loc, is_driver_available=is_driver_available)
            location.save()
            user = request.user
            if user.driver is None:
                user.driver = location
                user.save()
        return Response({'message': 'success', 'status': status.HTTP_200_OK})

    def update(self, request, *args, **kwargs):
        location = self.get_object()
        latitude = request.data.get('latitude', location.location.y)
        longitude = request.data.get('longitude', location.location.x)
        is_driver_available = request.data.get('is_driver_available', location.is_driver_available)

        # Create a new Point based on the updated latitude and longitude
        updated_location = Point(float(longitude), float(latitude), srid=4326)
        location.location = updated_location
        location.is_driver_available = is_driver_available
        location.save()
        return Response({'message': 'success', 'status': status.HTTP_200_OK})


class DriversListingView(viewsets.ModelViewSet):
    """
    Views for listing drivers for riders
    @param: driver id:str
    @return: dict:drive details:str
    """

    http_method_names = ['get', ]
    serializer_class = UserListingSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        drivers = self.queryset.filter(user_role='driver', driver__is_driver_available=True)
        user = self.request.user
        ride_obj = Ride.objects.filter(rider=user).last()
        if ride_obj and ride_obj.pickup_loc_latitude and ride_obj.pickup_loc_longitude:
            pickup_latitude = ride_obj.pickup_loc_latitude
            pickup_longitude = ride_obj.pickup_loc_longitude
            if pickup_latitude is None or pickup_longitude is None:
                return Response({"error": "Missing pickup location coordinates"})
            user_location = Point(float(pickup_longitude), float(pickup_latitude), srid=4326)

            # Query to find nearest drivers, Annotate the queryset with distance to the pickup location
            drivers = drivers.annotate(
                distance=Distance(F('driver__location'), user_location)
            ).order_by('distance')
        if drivers:
            serializer = self.serializer_class(drivers, many=True)
            return Response(serializer.data)
        return Response({'message': 'Drivers not found', 'status': status.HTTP_404_NOT_FOUND})
