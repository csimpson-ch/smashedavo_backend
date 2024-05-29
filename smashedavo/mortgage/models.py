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
        """Was the blog post published within the last seven days?
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
    loan_type = models.CharField(max_length=3, choices=LOAN_TYPE_CHOICES, default='MTG')
    start_date = models.DateField(default=timezone.now)

    # set the owner of the loan as user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username) + ' ' + str(self.loan_type) + ' ' + str(self.amount) 


class ExpenseInterval(models.Model):
    """Object representing a subscription that a user has.
    """
    # time intervals between subscription payments
    WEEKLY = 'WK'
    FORTNIGHTLY = 'FT'
    MONTHLY = 'MT'
    QUARTERLY = 'QT'
    ANNUAL = 'AN'
    OTHER = 'OT'
    INTERVAL_CHOICES = (
        (WEEKLY, 'Weekly'),
        (FORTNIGHTLY, 'Fortnightly'),
        (MONTHLY, 'Monthly'),
        (QUARTERLY, 'Quarterly'),
        (ANNUAL, 'Annual'),
        (OTHER, 'Other'),
    )

    # major categories for different types of subscriptions
    HOUSING = 'HOS'
    UTILITIES = 'UTI'
    INSURANCE = 'INS'
    EDUCATION = 'EDU'
    CHILDCARE = 'CHD'
    HEALTH = 'HLT'
    TRANSPORT = 'TRS'
    VEHICLE = 'VEH'
    TAXES = 'TAX'
    SUBSCRIPTION = 'SUB'
    OTHER = 'OTH'
    CATEGORY_CHOICES = (
        (HOUSING, 'Housing'),
        (UTILITIES, 'Utilities'),
        (INSURANCE, 'Insurance'),
        (EDUCATION, 'Education'),
        (CHILDCARE, 'Childcare'),
        (HEALTH, 'Health'),
        (TRANSPORT, 'Transport'),
        (VEHICLE, 'Vehicle'),
        (TAXES, 'Taxes'),
        (SUBSCRIPTION, 'Subscription'),
        (OTHER, 'Other'),
    )

    # set key details of this subscription
    description = models.CharField(max_length=50)
    amount = models.FloatField(default=10.0)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='OTH')
    interval = models.CharField(max_length=2, choices=INTERVAL_CHOICES, default='OTH')
    payments_per_year = models.IntegerField(default=12)
    next_payment_date = models.DateField(default=timezone.now)

    # set foreign key owner of this subscription
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'User: {self.user.username}, Description: {self.description}, Amount: {self.amount}, Payments per year: {self.payments_per_year}'


class ExpenseAdhoc(models.Model):
    """Object representing an individual expense.
    https://localfirstbank.com/article/budgeting-101-personal-budget-categories/?fb_content_cat=fb-tsm
    """
    # major categories for different types of subscriptions
    FOOD = 'FOD'
    CLOTHING = 'CLT'
    PERSONAL = 'PSL'
    ENTERTAINMENT = 'ENT'
    EDUCATION = 'EDU'
    CHILDCARE = 'CHD'
    GIFTS = 'GFT'
    INSURANCE = 'INS'
    HOUSING = 'HOS'
    UTILITIES = 'UTI'
    HEALTH = 'HLT'
    TRANSPORT = 'TRS'
    VEHICLE = 'VEH'
    TAXES = 'TAX'
    EMERGENCY = 'ECY'
    OTHER = 'OTH'
    CATEGORY_CHOICES = (
        (FOOD, 'Food'),
        (CLOTHING, 'Clothing'),
        (PERSONAL, 'Personal'),
        (ENTERTAINMENT, 'Entertainment'),
        (EDUCATION, 'Education'),
        (CHILDCARE, 'Childcare'),
        (GIFTS, 'Gifts'),
        (INSURANCE, 'Insurance'),
        (HOUSING, 'Housing'),
        (UTILITIES, 'Utilities'),
        (HEALTH, 'Health'),
        (TRANSPORT, 'Transport'),
        (VEHICLE, 'Vehicle'),
        (TAXES, 'Taxes'),
        (EMERGENCY, 'Emergency'),
        (OTHER, 'Other'),
    )

    # set key details of this subscription
    description = models.CharField(max_length=100)
    amount = models.FloatField()
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='OTH')
    date = models.DateField(default=timezone.now)

    # set foreign key owner of this subscription
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}, {self.description}, {self.amount}'

# TODO
# model for repaying part of a debt/loan
# model for investments/assets
# models for income (regular/interval and adhoc)

