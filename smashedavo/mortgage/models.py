from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class BlogPost(models.Model):
    """Blog Post object associated with one User object.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    pub_date = models.DateTimeField()

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title

    def was_published_recently(self):
        """Was the blog post published within the last seven days
        """
        was_published_recently = timezone.now() - datetime.timedelta(days=7) <= self.pub_date <= timezone.now()
        return was_published_recently


class Loan(models.Model):
    """Mortgage object associated with one User object.
    """
    MORTGAGE = 'MTG'
    HOME_EQUITY = 'HEQ'
    CAR = 'CAR'
    PERSONAL = 'PSL'
    STUDENT = 'STD'
    OTHER = 'OTH'
    LOAN_TYPE_CHOICES = (
        (MORTGAGE, 'Mortgage'),
        (HOME_EQUITY, 'Home Equity'),
        (CAR, 'Car'),
        (PERSONAL, 'Personal'),
        (STUDENT, 'Student'),
        (OTHER, 'Other'),
    )

    # required fields for loan
    amount = models.FloatField(default=200000)
    deposit = models.FloatField(default=10000.00)
    interest_rate = models.FloatField(default=5.00)
    paid_principal = models.FloatField(default=0.00)
    paid_interest = models.FloatField(default=0.00)
    loan_type = models.CharField(choices=LOAN_TYPE_CHOICES, default='MTG')
    start_date = models.DateField(default=timezone.now)

    # set the owner of the loan as user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount) + " " + str(self.user.username)


# class Subscriptions(models.Model):
#     """Object representing subscriptions that they have
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service = title = models.CharField(max_length=50)
#     interval = models.CharField(
#         max_length=3,
#         choices={
#             "WKL": "Weekly",
#             "FTN": "Fortnightly",
#             "MNT": "Monthly",
#             "ANL": "Annual",
#         },
#         default="MNT",
#     )
#     start_date = models.DateField(default=timezone.now(), blank=True)

#     def __str__():
#         return self.service