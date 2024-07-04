from django import forms 
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from formset.widgets import DateInput
from .models import Expense

class ExpenseForm(forms.ModelForm):
    '''Form for creating a new instance of the EventInterval model.
    '''
    # model fields
    # description = forms.CharField(max_length=100, required=True)

    # category = models.CharField(max_length=20, choices=EXPENSE_CHOICES, default='Other')
    # approved = models.BooleanField(default=True)
    # date = models.DateField(default=timezone.now)
    # loan_amount_principal = models.FloatField(default=0., blank=True, null=True)
    # loan_amount_interest = models.FloatField(default=0., blank=True, null=True)
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # regularpayment = models.ForeignKey(RegularPayment, blank=True, null=True, on_delete=models.CASCADE)
    # loan = models.ForeignKey(Loan, blank=True, null=True, on_delete=models.CASCADE)

    # 
    # amount = forms.FloatField(default=0., required=True)
    # category = forms.ChoiceField
    # approved = forms.BooleanField(default=True)
    # date = forms.DateField(default=timezone.now(), required=True)

    class Meta:
        model = Expense
        fields = ['description', 'amount', 'category', 'date', 'approved']
        # fields = "__all__"
