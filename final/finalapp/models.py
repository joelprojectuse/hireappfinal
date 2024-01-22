from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import User
import datetime
from django_jsonform.models.fields import ArrayField
from django.core.validators import RegexValidator

ROLE_CHOICES = (
    ("1", "jober"),
    ("2", "hirer"),
)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    # Add other fields you need
    role = models.CharField(
        max_length=15, choices=ROLE_CHOICES, default='jober')
    phone_number = models.CharField(max_length=15, blank=True, null=True, validators=[
                                    RegexValidator(r'^\d{10,15}$', message="Enter a valid phone number.")])
    name = models.CharField(max_length=150, default="Enter your name")
    ploc1 = models.CharField(max_length=150, default="none")
    ploc2 = models.CharField(max_length=150, default="none")

    # Provide unique related_name attributes to resolve the clashes
    groups = models.ManyToManyField(
        Group, related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='customuser_user_permissions', blank=True)

    """ def __str__(self):
        return self.username """


class Hiring(models.Model):
    manager_name = models.CharField(max_length=200)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_members = models.PositiveIntegerField()
    event_location = models.CharField(max_length=200)
    building_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        'finalapp.CustomUser', on_delete=models.CASCADE, null=False, blank=False)
    selected_user = ArrayField(
        models.CharField(max_length=40, blank=True),
        size=100, default=list
    )

    def __str__(self):
        return self.manager_name


class completed_jobs(models.Model):
    manager_name = models.CharField(max_length=200)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    event_location = models.CharField(max_length=200)
    attend_user = ArrayField(
        models.CharField(max_length=170, blank=True),
        size=100, default=list
    )

    def __str__(self):
        return self.manager_name


""" class job_selected(models.Model):
    manager_name = models.CharField(max_length=200)
    event_location = models.CharField(max_length=200)
    building_name = models.CharField(max_length=200)
    job_id = models.ForeignKey('finalapp.Hiring', on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        'finalapp.CustomUser', on_delete=models.CASCADE, null=False, blank=False)
    selected_user = ArrayField(
        models.CharField(max_length=40, blank=True),
        size=100
    ) """
