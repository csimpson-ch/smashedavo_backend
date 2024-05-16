from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    '''Inherits from built-in Django form specifically designed for user registration.
    The Meta class specifies the model to be used, which is the default Django User model.
    The fields attribute lists the fields that should be included in the form.
    '''
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class LoginForm(forms.Form):
    '''A standard Django form used for user login.
    It does not inherit from any specific Django form class.
    It defines two fields, username and password, using the forms.CharField() method.
    The password field is rendered as a password input field.
    '''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)