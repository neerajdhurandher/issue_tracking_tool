from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

# Create your models here.


class User(AbstractUser):
    organization_name = models.CharField(max_length=255,null=True)
