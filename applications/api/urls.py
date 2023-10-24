from django.conf.urls import url, include

from rest_framework import routers

from applications.api import views


router = routers.DefaultRouter()
router.register(r'^profile-create', views.ProfileCreateView, basename='profile-create'),
router.register(r'^ride', views.RideView, basename='ride'),
router.register(r'^ride-request', views.RideRequestView, basename='ride-request'),
router.register(r'^driver-listing', views.DriversListingView, basename='driver-listing'),
router.register(r'^driver-location', views.DriverLocationView, basename='driver-location'),


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/', views.LoginView.as_view(), name='login'),

]
