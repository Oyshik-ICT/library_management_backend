from django.db import models
from .choices import CategoryChoice

class Category(models.Model):
    name = models.CharField(max_length=20, choices=CategoryChoice.choices, unique=True)

class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)
    bio = models.TextField()

