from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models

from phonenumber_field.modelfields import PhoneNumberField


class DriverLocation(models.Model):
    location = gis_models.PointField(null=True, blank=True, geography=True)
    is_driver_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.location.x}, {self.location.y}"


class User(AbstractUser):
    ROLES = (
        ('driver', 'Driver'),
        ('rider', 'Rider')
    )
    full_name = models.CharField(max_length=125, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    user_role = models.CharField(max_length=125, null=True, blank=True, choices=ROLES)
    driver = gis_models.OneToOneField(DriverLocation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username

