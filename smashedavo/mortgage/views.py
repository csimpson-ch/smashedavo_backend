from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm

# Create your views here.
def index(request):
    '''This view represents the home page of your application.
    It renders the 'index.html' template and returns it as a response.
    '''
    # template = loader.get_template("mortgage/index.html")
    # context = {}
    # return HttpResponse(template.render(context, request))
    return render(request, "mortgage/index.html")


def user_signup(request):
    '''This view handles the signup page.
    It checks if the request method is POST, which indicates a form submission.
    If so, it validates the submitted form data using UserCreationForm.
    If the form is valid, it saves the user and redirects them to the login page.
    If the request method is GET, it creates a new instance of UserCreationForm and
        renders the 'signup.html' template, passing the form as context.
    '''
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'mortgage/signup.html', {'form': form})


def user_login(request):
    '''This view handles the login page. 
    It checks if the request method is POST, indicating a form submission.
    It validates the submitted form data using LoginForm.
    If the form is valid, it retrieves the username and password from the cleaned data.
    It then authenticates the user using authenticate() and logs them in using login().
    If the user is successfully authenticated, it redirects them to the home page.
    If the request method is GET, it creates a new instance of LoginForm and 
        renders the 'login.html' template, passing the form as context.
    '''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)    
                return redirect('login_success')
    else:
        form = LoginForm()
    return render(request, 'mortgage/login.html', {'form': form})


def user_logout(request):
    '''
    This view handles the logout functionality. 
    It calls the logout() function provided by Django to log out the user
        and redirects them to the login page.
    '''
    logout(request)
    return redirect('index')