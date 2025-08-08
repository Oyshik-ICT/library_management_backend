from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    penalty_points = models.IntegerField(default=0)

    def __str__(self):
        return self.username
