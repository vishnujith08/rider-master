from django.contrib import admin

from applications.ride.models import Ride, RideRequest


admin.site.register(Ride)
admin.site.register(RideRequest)
