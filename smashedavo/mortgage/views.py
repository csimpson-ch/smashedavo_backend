from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.template import loader
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


class BlogPostListView(ListView):
    '''By default, will use template_name of mortgage/blogpost_list.html
    '''
    model = BlogPost

    def get_queryset(self):
        '''Return only blog posts with pub_date now or in the past.
        '''
        blog_post_pub_date_in_past = BlogPost.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")
        return blog_post_pub_date_in_past


class BlogPostDetailView(DetailView):
    '''By default, uses template_name of mortgage/blogpost_detail.html
    '''
    model = BlogPost


class LoanListView(ListView):
    '''By default, will use template name of mortgage/loan_list.html
    '''
    model = Loan

    def get_queryset(self):
        '''Returns all loans belonging to this user, ordered by start date.
        '''
        loans_belonging_to_user = Loan.objects.filter(user=self.request.user)
        return loans_belonging_to_user.order_by("-start_date")[:]


class ExpenseIntervalListView(ListView):
    '''By default, will use template name of mortgage/expenseinterval_list.html
    '''
    model = ExpenseInterval

    def get_queryset(self):
        '''Returns all expenses (interval), ordered by next payment date in ascending order.
        '''
        belonging_to_user = ExpenseInterval.objects.filter(user=self.request.user)
        return belonging_to_user.order_by("next_payment_date")[:]


class ExpenseAdhocListView(ListView):
    '''By default, will use template name of mortgage/expenseadhoc_list.html
    '''
    model = ExpenseAdhoc

    def get_queryset(self):
        '''Returns all expenses, ordered by date in descending order.
        '''
        belonging_to_user = ExpenseAdhoc.objects.filter(user=self.request.user)
        return belonging_to_user.order_by("-date")[:]


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


def create(request):
    '''This view handles rendering the create.html template.
    '''
    return render(request, 'mortgage/create.html', {})


@login_required()
def blog_create(request):
    '''Creates a new blog post object based on model form.
    '''
    # if a get request, show blank form
    if request.method == "GET":
        form = BlogForm()
    
    # if post, attempt to create new mortgage object using completed form
    elif request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.user = request.user
            blogpost.save()
            return redirect(reverse("mortgage:blog_list", args=()))

    # if here, must be invalid form or get request
    return render(request, "mortgage/blogpost_create.html", {"form": form})


def blog_delete(request, blogpost_id):
    '''Delete blog post with specific id.
    GET: check that user wants to delete the blog post.
    POST: delete the object and redirect to blog list.
    '''
    blogpost = BlogPost.objects.get(pk=blogpost_id)
    if request.method == 'GET':        
        return render(request, 'mortgage/blogpost_delete.html', {'blogpost': blogpost})
    elif request.method == "POST":
        blogpost.delete()
        return redirect(reverse("mortgage:blog_list", args=()))
    
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
        return render(request, 'mortgage/blogpost_edit.html', {'blogpost': blogpost, 'form': form})
    elif request.method == 'POST':
        form = BlogForm(request.POST, instance=blogpost)
        if form.is_valid():
            form.save()
            return redirect(reverse("mortgage:blog_list", args=()))

    # TODO - replace with 404?
    return HttpResponseNotFound('This is not a valid operation')


def loan_create(request):
    """Creates a new loan object based on model form.
    """
    # if a get reuqest, show blank form
    if request.method == "GET":
        form = LoanForm()
    
    # if post, attempt to create new object using completed form
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


def expenseinterval_create(request):
    """Creates a new expense (interval) object based on model form.
    """
    # if a get reuqest, show blank form
    if request.method == "GET":
        form = ExpenseIntervalForm()
    
    # if post, attempt to create new object using completed form
    elif request.method == "POST":
        form = ExpenseIntervalForm(request.POST)
        if form.is_valid():
            expenseinterval = form.save(commit=False)
            expenseinterval.user = request.user
            expenseinterval.next_payment_date = form.cleaned_data['next_payment_date']
            expenseinterval.save()
            return redirect(reverse("mortgage:expenseinterval_list", args=()))

    # if here, must be invalid form or get request
    return render(request, "mortgage/expenseinterval_create.html", {"form": form})


def expenseinterval_delete(request, expenseinterval_id):
    '''Delete existing expense (interval) object.
    '''
    if request.method == "POST":
        expenseinterval = ExpenseInterval.objects.get(pk=expenseinterval_id)
        expenseinterval.delete()
        return HttpResponseRedirect(reverse("mortgage:expenseinterval_list", args=()))
    
    # TODO - replace with 404 or other error?
    return HttpResponseNotFound('This is not a valid operation')


def expenseinterval_edit(request, expenseinterval_id):
    '''Update details of existing expenseinterval object.
    GET: prepopulate form with existing details.
    POST: update details of existing object.
    '''
    expenseinterval = ExpenseInterval.objects.get(pk=expenseinterval_id)
    if request.method == 'GET':
        form = ExpenseIntervalForm(instance=expenseinterval)
    elif request.method == 'POST':
        form = ExpenseIntervalForm(request.POST, instance=expenseinterval)     
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("mortgage:expenseinterval_list", args=()))
    return render(request, 'mortgage/expenseinterval_edit.html', {'form': form, 'expenseinterval': expenseinterval})


def expenseadhoc_create(request):
    """Creates a new expense (ad hoc) object based on model form.
    """
    # if a get reuqest, show blank form
    if request.method == "GET":
        form = ExpenseAdhocForm()
    
    # if post, attempt to create new object using completed form
    elif request.method == "POST":
        form = ExpenseAdhocForm(request.POST)
        if form.is_valid():
            expenseadhoc = form.save(commit=False)
            expenseadhoc.user = request.user
            expenseadhoc.date = form.cleaned_data['date']
            expenseadhoc.save()
            return redirect(reverse("mortgage:expenseadhoc_list", args=()))

    # if here, must be invalid form or get request
    return render(request, "mortgage/expenseadhoc_create.html", {"form": form})


def expenseadhoc_delete(request, expenseadhoc_id):
    '''Delete existing expense (ad hoc) object.
    '''
    if request.method == "POST":
        expenseadhoc = ExpenseAdhoc.objects.get(pk=expenseadhoc_id)
        expenseadhoc.delete()
        return HttpResponseRedirect(reverse("mortgage:expenseadhoc_list", args=()))
    
    # TODO - replace with 404 or other error?
    return HttpResponseNotFound('This is not a valid operation')


def expenseadhoc_edit(request, expenseadhoc_id):
    '''Update details of existing expenseadhoc object.
    GET: prepopulate form with existing details.
    POST: update details of existing object.
    '''
    expenseadhoc = ExpenseAdhoc.objects.get(pk=expenseadhoc_id)
    if request.method == 'GET':
        form = ExpenseAdhocForm(instance=expenseadhoc)
    elif request.method == 'POST':
        form = ExpenseAdhocForm(request.POST, instance=expenseadhoc)     
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("mortgage:expenseadhoc_list", args=()))
    return render(request, 'mortgage/expenseadhoc_edit.html', {'form': form, 'expenseadhoc': expenseadhoc})
