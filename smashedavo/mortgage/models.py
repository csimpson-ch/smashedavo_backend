from django.db import models

# Create your models here.
class User(models.Model):
    """user model for basic site users
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    email = models.EmailField()
    dob = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Mortgage(models.Model):
    """A User can be associated with many Mortgage objects
    But a mortgage can only have one User object.
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

