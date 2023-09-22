from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    total_users = models.PositiveIntegerField(default=0)
