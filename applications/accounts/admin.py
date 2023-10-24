from django.contrib import admin

from applications.accounts.models import User, DriverLocation


admin.site.register(User)
admin.site.register(DriverLocation)
