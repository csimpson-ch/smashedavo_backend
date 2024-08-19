from django import forms
from .models import Expense, RegularPayment

class ExpenseForm(forms.ModelForm):
    '''Form for creating a new instance of the EventInterval model.
    '''
    class Meta:
        model = Expense
        # fields = ['description', 'amount', 'category', 'date', 'approved']
        fields = "__all__"


class RegularPaymentForm(forms.ModelForm):
    '''Form for creating a new instance of the model.
    '''
    class Meta:
        model = RegularPayment
        fields = ['description', 'amount', 'category', 'interval', 'first_payment_date', 'next_payment_date']
        # fields = "__all__"
