from django.contrib.gis.db import models

from applications.accounts.models import User


class Ride(models.Model):
    STATUSES = (
        ('completed', 'Completed'),
        ('running', 'Running'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')
    )
    rider = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='rides')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    pickup_loc_latitude = models.CharField(max_length=255, null=True, blank=True)
    pickup_loc_longitude = models.CharField(max_length=255, null=True, blank=True)
    dropoff_loc_latitude = models.CharField(max_length=255, null=True, blank=True)
    dropoff_loc_logitude = models.CharField(max_length=255, null=True, blank=True)
    current_location = models.PointField(null=True, blank=True)
    status = models.CharField(max_length=60, null=True, blank=True, choices=STATUSES)
    ride_review = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.rider.username


class RideRequest(models.Model):
    STATUSES = (
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled')
    )
    driver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUSES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ride.rider.username
