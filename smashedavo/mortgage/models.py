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
    LOAN_TYPE_CHOICES = (
        ('Mortgage', 'Mortgage'),
        ('Home Equity', 'Home Equity'),
        ('Car', 'Car'),
        ('Personal', 'Personal'),
        ('Student', 'Student'),
        ('Other', 'Other'),
    )

    # required fields for loan
    description = models.CharField(default='description', max_length=50)
    amount = models.FloatField(default=10000)
    interest_rate = models.FloatField(default=5.00)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE_CHOICES, default='Other')
    start_date = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)

    # TODO - remove these as they can be derived from individual payments made to loan.
    # amount_remaining = models.FloatField(default=180000)
    # paid_principal = models.FloatField(default=0.00)
    # paid_interest = models.FloatField(default=0.00)

    # set foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'User: {self.user.username}, Description: {self.description}' 


class ExpenseInterval(models.Model):
    """Object representing a subscription that a user has.
    """
    # time intervals between subscription payments
    INTERVAL_CHOICES = (
        ('Weekly', 'Weekly'),
        ('Fortnightly', 'Fortnightly'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annual', 'Annual'),
    )

    # major categories for different types of expenses
    EXPENSE_CHOICES = (
        ('Food', 'Food'),
        ('Clothing', 'Clothing'),
        ('Personal', 'Personal'),
        ('Entertainment', 'Entertainment'),
        ('Subscription', 'Subscription'),
        ('Transport', 'Transport'),
        ('Education', 'Education'),
        ('Health', 'Health'),
        ('Childcare', 'Childcare'),
        ('Gift', 'Gift'),
        ('Housing', 'Housing'),
        ('Utilities', 'Utilities'),
        ('Insurance', 'Insurance'),
        ('Vehicle', 'Vehicle'),
        ('Taxes', 'Taxes'),
        ('Emergency', 'Emergency'),
        ('Other', 'Other'),
    )

    # set key details of this subscription
    description = models.CharField(max_length=50)
    amount = models.FloatField(default=10.0)
    category = models.CharField(max_length=20, choices=EXPENSE_CHOICES, default='Other')
    interval = models.CharField(max_length=20, choices=INTERVAL_CHOICES, default='Monthly')
    payments_per_year = models.IntegerField(default=12)
    next_payment_date = models.DateField(default=timezone.now)
    last_payment_date = models.DateField(default=timezone.now)

    # set foreign key owner of this subscription
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Description: {self.description}, Amount: {self.amount}, Interval: {self.interval}, Next Payment: {self.next_payment_date}\n '


class ExpenseAdhoc(models.Model):
    """Object representing a specific expense.
    """
    # major categories for different types of expenses
    EXPENSE_CHOICES = (
        ('Food', 'Food'),
        ('Clothing', 'Clothing'),
        ('Personal', 'Personal'),
        ('Entertainment', 'Entertainment'),
        ('Subscription', 'Subscription'),
        ('Transport', 'Transport'),
        ('Education', 'Education'),
        ('Health', 'Health'),
        ('Childcare', 'Childcare'),
        ('Gift', 'Gift'),
        ('Housing', 'Housing'),
        ('Utilities', 'Utilities'),
        ('Insurance', 'Insurance'),
        ('Vehicle', 'Vehicle'),
        ('Taxes', 'Taxes'),
        ('Emergency', 'Emergency'),
        ('Other', 'Other'),
    )

    # set required details of this expense
    description = models.CharField(max_length=100)
    amount = models.FloatField(default=0.)
    category = models.CharField(max_length=20, choices=EXPENSE_CHOICES, default='Other')
    approved = models.BooleanField(default=True)
    date = models.DateField(default=timezone.now)

    # set optional fields
    loan_amount_principal = models.FloatField(default=0., blank=True, null=True)
    loan_amount_interest = models.FloatField(default=0., blank=True, null=True)

    # set foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expenseinterval = models.ForeignKey(ExpenseInterval, blank=True, null=True, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.description}, {self.amount}, {self.date}'

# TODO
# model for repaying part of a debt/loan
# model for investments/assets
# models for income (regular/interval and adhoc)

