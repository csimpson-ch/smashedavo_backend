from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from formset.widgets import DateInput, DateTimeInput
from .models import BlogPost, Loan


class SignupForm(UserCreationForm):
    '''Inherits from built-in Django form designed for user registration.
    '''
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        '''The Meta class specifies to use the default Django User model.
        '''
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        '''These fields require special setup to bootstrapify them.
        '''
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    '''A standard Django form used for user login, with a password input field.
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class BlogForm(forms.ModelForm):
    '''Form for creating a new instance of the BlogPost model.
    '''
    pub_date = forms.DateTimeField(widget=DateTimeInput)

    class Meta:
        model = BlogPost
        # fields = "__all__"
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class LoanForm(forms.ModelForm):
    '''Form for creating a new instance of the Loan model.
    '''
    start_date = forms.DateField(widget=DateInput)

    class Meta:
        model = Loan
        # fields = "__all__"
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(LoanForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        

