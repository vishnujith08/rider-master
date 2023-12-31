# Generated by Django 3.2 on 2023-10-21 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_loc_latitude', models.CharField(blank=True, max_length=255, null=True)),
                ('pickup_loc_longitude', models.CharField(blank=True, max_length=255, null=True)),
                ('dropoff_loc_latitude', models.CharField(blank=True, max_length=255, null=True)),
                ('dropoff_loc_logitude', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, choices=[('completed', 'Completed'), ('running', 'Running'), ('pending', 'Pending'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], max_length=60, null=True)),
                ('ride_review', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('rider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rides', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RideRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('success', 'Success'), ('pending', 'Pending'), ('cancelled', 'Cancelled')], max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('drivers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('ride', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ride.ride')),
            ],
        ),
    ]
