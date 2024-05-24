from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.template import loader
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm, BlogForm, LoanForm
from .models import BlogPost, Loan


class BlogPostListView(ListView):
    '''By default, will use template_name of mortgage/blogpost_list.html
    '''
    model = BlogPost


class BlogPostDetailView(DetailView):
    '''By default, uses template_name of mortgage/blogpost_detail.html
    '''
    model = BlogPost


class LoanListView(ListView):
    '''By default, will use template name of mortgage/loan_list.html
    '''
    model = Loan

    def get_queryset(self):
        '''Returns all loans, ordered by start date.
        '''
        loans_belonging_to_user = Loan.objects.filter(user=self.request.user)
        return loans_belonging_to_user.order_by("-start_date")[:]


def index(request):
    '''This view represents the home page of your application.
    It renders the 'index.html' template and returns it as a response.
    '''
    return render(request, "mortgage/index.html")


def user_signup(request):
    '''This view handles the signup page.
    It checks if the request method is POST, which indicates a form submission.
    If so, it validates the submitted form data using SignupForm.
    If the form is valid, it saves the user and redirects them to the login page.
    If the request method is GET, it creates a new instance of SignupForm and
        renders the 'signup.html' template, passing the form as context.
    '''
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("mortgage:login", args=()))
        else:
            return render(request, 'mortgage/signup.html', {'form': form, 'failed': 'username already exists'})
    elif request.method == 'GET':
        form = SignupForm()
        return render(request, 'mortgage/signup.html', {'form': form, 'failed': None})


def user_login(request, failed=None):
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
                return HttpResponseRedirect(reverse("mortgage:index", args=()))
            else:
                return render(request, 'mortgage/login.html', {'form': form, 'failed': True})
    else:
        form = LoginForm()
        return render(request, 'mortgage/login.html', {'form': form, 'failed': None})


def user_logout(request):
    '''
    This view handles the logout functionality. 
    It calls the logout() function provided by Django to log out the user
        and redirects them to the login page.
    '''
    logout(request)
    return HttpResponseRedirect(reverse("mortgage:index", args=()))


@login_required()
def blog_create(request):
    '''Creates a new blog post object based on model form.
    '''
    # if a get reuqest, show blank form
    if request.method == "GET":
        form = BlogForm()
    
    # if post, attempt to create new mortgage object using completed form
    elif request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.user = request.user
            blogpost.save()
            return HttpResponseRedirect(reverse("mortgage:blog_list", args=()))

    # if here, must be invalid form or get request
    return render(request, "mortgage/blogpost_create.html", {"form": form})


def blog_delete(request, blogpost_id):
    if request.method == "POST":
        blogpost = BlogPost.objects.get(pk=blogpost_id)
        blogpost.delete()
        return HttpResponseRedirect(reverse("mortgage:blog_list", args=()))
    
    # TODO - replace with 404?
    return HttpResponseNotFound('This is not a valid operation')


def blog_edit(request, blogpost_id):
    '''Update details of existing BlogPost object.
    GET: render the pre-fill with existing content.
    POST: update the blog post details and re-direct to blog list.
    '''
    blogpost = BlogPost.objects.get(pk=blogpost_id)
    if request.method == 'GET':
        form = BlogForm(instance=blogpost)
    elif request.method == 'POST':
        form = BlogForm(request.POST, instance=blogpost)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("mortgage:blog_list", args=()))
    return render(request, 'mortgage/blogpost_edit.html', {'form': form})


def loan_create(request):
    """Creates a new loan object based on model form.
    """
    # if a get reuqest, show blank form
    if request.method == "GET":
        form = LoanForm()
    
    # if post, attempt to create new mortgage object using completed form
    elif request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.user = request.user
            loan.start_date = form.cleaned_data['start_date']
            loan.save()
            return redirect(reverse("mortgage:loan_list", args=()))

    # if here, must be invalid form or get request
    return render(request, "mortgage/loan_create.html", {"form": form})


def loan_delete(request, loan_id):
    '''Delete existing loan object.
    '''
    if request.method == "POST":
        loan = Loan.objects.get(pk=loan_id)
        loan.delete()
        return HttpResponseRedirect(reverse("mortgage:loan_list", args=()))
    
    # TODO - replace with 404 or other error?
    return HttpResponseNotFound('This is not a valid operation')


def loan_edit(request, loan_id):
    '''Update details of existing loan object.
    GET: prepopulate form with existing details.
    POST: update details of existing object.
    '''
    loan = Loan.objects.get(pk=loan_id)
    if request.method == 'GET':
        form = LoanForm(instance=loan)
    elif request.method == 'POST':
        form = LoanForm(request.POST, instance=loan)     
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("mortgage:loan_list", args=()))
    return render(request, 'mortgage/loan_edit.html', {'form': form, 'loan': loan})
