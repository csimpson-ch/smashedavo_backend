from django.db import models

# Create your models here.
class Users(models.Model):
    """user model for basic site users
    """
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
