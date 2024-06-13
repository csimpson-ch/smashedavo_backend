from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import datetime


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, first_name, last_name, password=None):
        user = self.model(
            username=username,
            email=email,            
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.set_password(password)
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None):
        user = self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self):
        return self.get(self.username)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, default='username')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    # set the object manager
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def natural_key(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class BlogPost(models.Model):
    """Blog Post object associated with one User object.
    """
    title = models.CharField(max_length=100)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

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

    # set foreign keys
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    expenseinterval = models.ForeignKey(ExpenseInterval, blank=True, null=True, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.description}, {self.amount}, {self.date}'

# TODO
# model for repaying part of a debt/loan
# model for investments/assets
# models for income (regular/interval and adhoc)
