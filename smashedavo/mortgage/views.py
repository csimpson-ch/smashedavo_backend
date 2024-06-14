# import os
# from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound, JsonResponse
# from django.core import serializers as django_serializers
# from rest_framework import serializers as rest_framework_serializers
# from django.template import loader
# from django.shortcuts import render, reverse, redirect, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth import authenticate, login, logout 
# from django.views.generic import ListView, DetailView
# from django.contrib.auth.decorators import login_required
# from django.db.models import Sum

# from .forms import *
# from .models import *

# import datetime
# from dateutil.relativedelta import *


# class BlogPostSerializer(rest_framework_serializers.ModelSerializer):
#     '''Use the rest framework serializer to create custom class
#     '''
#     user = rest_framework_serializers.CharField(source ='user.username')
#     pub_date = rest_framework_serializers.DateTimeField(format="%Y-%m-%d")

#     class Meta:
#         model = BlogPost
#         fields = '__all__'
#         # fields = ['id', 'title', 'text', 'pub_date', 'user']


# def backend_get_all_blogposts(request):
#     # blogposts_as_json = BlogPostSerializer(BlogPost.objects.all(), many=True).data
#     blogposts_as_json = django_serializers.serialize('json', BlogPost.objects.all(), cls=BlogPostSerializer)
#     return HttpResponse(blogposts_as_json, content_type='application/json')



# '''TODO - imported from capstone
#     # set backend url from environment variable
#     backend_url = os.getenv('backend_url', default="http://localhost:8000")


#     def get_request(endpoint, **kwargs):
#         params = ""
#         if (kwargs):
#             for key, value in kwargs.items():
#                 params = params+key+"="+value+"&"
#         request_url = backend_url+endpoint+"?"+params
#         print("GET from {} ".format(request_url))
#         try:
#             # Call get method of requests library with URL and parameters
#             response = requests.get(request_url)
#             return response.json()
#         except Exception as err:
#             print(f"Unexpected {err=}, {type(err)=}")
#             print("Network exception occurred")
# '''


# class BlogPostListView(ListView):
#     '''By default, will use template_name of mortgage/blogpost_list.html
#     '''
#     model = BlogPost

#     def get_queryset(self):
#         '''Return only blog posts with pub_date now or in the past.
#         '''
#         blog_post_pub_date_in_past = BlogPost.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")
#         return blog_post_pub_date_in_past


# class BlogPostDetailView(DetailView):
#     '''By default, uses template_name of mortgage/blogpost_detail.html
#     '''
#     model = BlogPost


# class LoanListView(ListView):
#     '''By default, will use template name of mortgage/loan_list.html
#     '''
#     model = Loan

#     def get_queryset(self):
#         '''Returns all loans belonging to this user, ordered by start date.
#         '''
#         loans_belonging_to_user = Loan.objects.filter(user=self.request.user)
#         return loans_belonging_to_user.order_by("-start_date")[:]


# class ExpenseIntervalListView(ListView):
#     '''By default, will use template name of mortgage/expenseinterval_list.html
#     '''
#     model = ExpenseInterval

#     def get_queryset(self):
#         '''Returns all expenses (interval), ordered by next payment date in ascending order.
#         '''
#         belonging_to_user = ExpenseInterval.objects.filter(user=self.request.user)
#         return belonging_to_user.order_by("next_payment_date")[:]


# class ExpenseAdhocListView(ListView):
#     '''By default, will use template name of mortgage/expenseadhoc_list.html
#     '''
#     model = ExpenseAdhoc

#     def get_queryset(self):
#         '''Returns all expenses, ordered by date in descending order.
#         '''
#         belonging_to_user = ExpenseAdhoc.objects.filter(user=self.request.user)
#         return belonging_to_user.order_by("-date")[:]


# def index(request):
#     '''This view represents the home page of your application.
#     It renders the 'index.html' template and returns it as a response.
#     '''
#     return render(request, "mortgage/index.html")


# def user_signup(request):
#     '''This view handles the signup page.
#     It checks if the request method is POST, which indicates a form submission.
#     If so, it validates the submitted form data using SignupForm.
#     If the form is valid, it saves the user and redirects them to the login page.
#     If the request method is GET, it creates a new instance of SignupForm and
#         renders the 'signup.html' template, passing the form as context.
#     '''
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("mortgage:login", args=()))
#         else:
#             return render(request, 'mortgage/signup.html', {'form': form, 'failed': 'username already exists'})
#     elif request.method == 'GET':
#         form = SignupForm()
#         return render(request, 'mortgage/signup.html', {'form': form, 'failed': None})


# def user_login(request, failed=None):
#     '''This view handles the login page. 
#     It checks if the request method is POST, indicating a form submission.
#     It validates the submitted form data using LoginForm.
#     If the form is valid, it retrieves the username and password from the cleaned data.
#     It then authenticates the user using authenticate() and logs them in using login().
#     If the user is successfully authenticated, it redirects them to the home page.
#     If the request method is GET, it creates a new instance of LoginForm and 
#         renders the 'login.html' template, passing the form as context.
#     '''
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse("mortgage:index", args=()))
#             else:
#                 return render(request, 'mortgage/login.html', {'form': form, 'failed': True})
#     else:
#         form = LoginForm()
#         return render(request, 'mortgage/login.html', {'form': form, 'failed': None})


# def user_logout(request):
#     '''
#     This view handles the logout functionality. 
#     It calls the logout() function provided by Django to log out the user
#         and redirects them to the login page.
#     '''
#     logout(request)
#     return HttpResponseRedirect(reverse("mortgage:index", args=()))


# def create(request):
#     '''This view handles rendering the create.html template.
#     '''
#     return render(request, 'mortgage/create.html', {})


# @login_required()
# def blog_create(request):
#     '''Creates a new blog post object based on model form.
#     '''
#     # if a get request, show blank form
#     if request.method == "GET":
#         form = BlogForm()
    
#     # if post, attempt to create new mortgage object using completed form
#     elif request.method == "POST":
#         form = BlogForm(request.POST)
#         if form.is_valid():
#             blogpost = form.save(commit=False)
#             blogpost.user = request.user
#             blogpost.save()
#             return redirect(reverse("mortgage:blog_list", args=()))

#     # if here, must be invalid form or get request
#     return render(request, "mortgage/blogpost_create.html", {"form": form})


# def blog_delete(request, blogpost_id):
#     '''Delete blog post with specific id.
#     GET: check that user wants to delete the blog post.
#     POST: delete the object and redirect to blog list.
#     '''
#     blogpost = BlogPost.objects.get(pk=blogpost_id)
#     if request.method == 'GET':        
#         return render(request, 'mortgage/blogpost_delete.html', {'blogpost': blogpost})
#     elif request.method == "POST":
#         blogpost.delete()
#         return redirect(reverse("mortgage:blog_list", args=()))
    
#     # TODO - replace with 404?
#     return HttpResponseNotFound('This is not a valid operation')


# def blog_edit(request, blogpost_id):
#     '''Update details of existing BlogPost object.
#     GET: render the pre-fill with existing content.
#     POST: update the blog post details and re-direct to blog list.
#     '''
#     blogpost = BlogPost.objects.get(pk=blogpost_id)
#     if request.method == 'GET':
#         form = BlogForm(instance=blogpost)
#         return render(request, 'mortgage/blogpost_edit.html', {'blogpost': blogpost, 'form': form})
#     elif request.method == 'POST':
#         form = BlogForm(request.POST, instance=blogpost)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse("mortgage:blog_list", args=()))

#     # TODO - replace with 404?
#     return HttpResponseNotFound('This is not a valid operation')


# def loan_create(request):
#     """Creates a new loan object based on model form.
#     """
#     # if a get reuqest, show blank form
#     if request.method == "GET":
#         form = LoanForm()
    
#     # if post, attempt to create new object using completed form
#     elif request.method == "POST":
#         form = LoanForm(request.POST)
#         if form.is_valid():
#             loan = form.save(commit=False)
#             loan.user = request.user
#             loan.start_date = form.cleaned_data['start_date']
#             loan.save()
#             return redirect(reverse("mortgage:loan_list", args=()))

#     # if here, must be invalid form or get request
#     return render(request, "mortgage/loan_create.html", {"form": form})


# # def loan_detail(request, loan_id=None):
# #     '''Displays details of loan and associated expenses (adhoc).
# #     TODO - handle loan object is null
# #     '''
# #     if loan_id is not None:
# #         loan = Loan.objects.get(pk=loan_id)
# #         expensesinterval = loan.expenseinterval_set.all()
# #         expensesadhoc = loan.expenseadhoc_set.all().order_by('-date')
# #         return render(request, 'mortgage/loan_detail.html', {'loan': loan, 'expensesadhoc': expensesadhoc, 'expensesinterval': expensesinterval})
# #     return HttpResponse('Null')


# def loan_payment(request, loan_id):
#     '''Displays payments and other details associated with loan.
#     '''
#     loan = Loan.objects.get(pk=loan_id)
#     expensesinterval = loan.expenseinterval_set.all()
#     expensesadhoc = loan.expenseadhoc_set.all().order_by('-date')
#     total_principal = loan.expenseadhoc_set.filter(approved=True).aggregate(total_principal=Sum('loan_amount_principal'))
#     total_interest = loan.expenseadhoc_set.filter(approved=True).aggregate(total_interest=Sum('loan_amount_interest'))
#     dict_to_pass = {
#         'loan': loan,
#         'total_principal': total_principal,
#         'total_interest': total_interest,
#         'expensesadhoc': expensesadhoc,
#         'expensesinterval': expensesinterval,
#     }
#     return render(
#         request,
#         'mortgage/loan_payment.html', 
#         dict_to_pass,
#     )


# def loan_delete(request, loan_id):
#     '''Delete existing loan object.
#     '''
#     if request.method == "POST":
#         loan = Loan.objects.get(pk=loan_id)
#         loan.delete()
#         return HttpResponseRedirect(reverse("mortgage:loan_list", args=()))
    
#     # TODO - replace with 404 or other error?
#     return HttpResponseNotFound('This is not a valid operation')


# def loan_edit(request, loan_id):
#     '''Update details of existing loan object.
#     GET: prepopulate form with existing details.
#     POST: update details of existing object.
#     '''
#     loan = Loan.objects.get(pk=loan_id)
#     if request.method == 'GET':
#         form = LoanForm(instance=loan)
#     elif request.method == 'POST':
#         form = LoanForm(request.POST, instance=loan)     
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("mortgage:loan_list", args=()))
#     return render(request, 'mortgage/loan_edit.html', {'form': form, 'loan': loan})


# def expenseinterval_create(request):
#     """Creates a new expense (interval) object based on model form.
#     """
#     # if a get reuqest, show blank form
#     if request.method == "GET":
#         form = ExpenseIntervalForm()
    
#     # if post, attempt to create new object using completed form
#     elif request.method == "POST":
#         form = ExpenseIntervalForm(request.POST)
#         if form.is_valid():
#             expenseinterval = form.save(commit=False)
#             expenseinterval.user = request.user
#             expenseinterval.next_payment_date = form.cleaned_data['next_payment_date']
#             expenseinterval.save()
#             return redirect(reverse("mortgage:expenseinterval_list", args=()))

#     # if here, must be invalid form or get request
#     return render(request, "mortgage/expenseinterval_create.html", {"form": form})


# def expenseinterval_details(request, expenseinterval_id=None):
#     '''Displays details of expense (interval) and associated expenses (adhoc).
#     TODO - handle expense (interval) object is null
#     '''
#     if expenseinterval_id is not None:
#         expenseinterval = ExpenseInterval.objects.get(pk=expenseinterval_id)
#         expensesadhoc = expenseinterval.expenseadhoc_set.all()
#         return render(request, 'mortgage/expenseinterval_details.html', {'expenseinterval': expenseinterval, 'expensesadhoc': expensesadhoc})
#     return HttpResponse('Null')


# def expenseinterval_delete(request, expenseinterval_id):
#     '''Delete existing expense (interval) object.
#     '''
#     if request.method == "POST":
#         expenseinterval = ExpenseInterval.objects.get(pk=expenseinterval_id)
#         expenseinterval.delete()
#         return HttpResponseRedirect(reverse("mortgage:expenseinterval_list", args=()))
    
#     # TODO - replace with 404 or other error?
#     return HttpResponseNotFound('This is not a valid operation')


# def expenseinterval_edit(request, expenseinterval_id):
#     '''Update details of existing expenseinterval object.
#     GET: prepopulate form with existing details.
#     POST: update details of existing object.
#     '''
#     expenseinterval = ExpenseInterval.objects.get(pk=expenseinterval_id)
#     if request.method == 'GET':
#         form = ExpenseIntervalForm(instance=expenseinterval)
#     elif request.method == 'POST':
#         form = ExpenseIntervalForm(request.POST, instance=expenseinterval)     
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("mortgage:expenseinterval_list", args=()))
#     return render(request, 'mortgage/expenseinterval_edit.html', {'form': form, 'expenseinterval': expenseinterval})


# def expenseadhoc_create(request):
#     """Creates a new expense (ad hoc) object based on model form.
#     """
#     # if a get reuqest, show blank form
#     if request.method == "GET":
#         form = ExpenseAdhocForm()
    
#     # if post, attempt to create new object using completed form
#     elif request.method == "POST":
#         form = ExpenseAdhocForm(request.POST)
#         if form.is_valid():
#             expenseadhoc = form.save(commit=False)
#             expenseadhoc.user = request.user
#             expenseadhoc.date = form.cleaned_data['date']
#             expenseadhoc.save()
#             return redirect(reverse("mortgage:expenseadhoc_list", args=()))

#     # if here, must be invalid form or get request
#     return render(request, "mortgage/expenseadhoc_create.html", {"form": form})


# def expenseadhoc_delete(request, expenseadhoc_id):
#     '''Delete existing expense (ad hoc) object.
#     '''
#     if request.method == "POST":
#         expenseadhoc = ExpenseAdhoc.objects.get(pk=expenseadhoc_id)
#         expenseadhoc.delete()
#         return HttpResponseRedirect(reverse("mortgage:for_approval", kwargs={'error': False}))
    
#     # TODO - replace with 404 or other error?
#     return HttpResponseNotFound('This is not a valid operation')


# def expenseadhoc_edit(request, expenseadhoc_id):
#     '''Update details of existing expenseadhoc object.
#     GET: prepopulate form with existing details.
#     POST: update details of existing object.
#     '''
#     expenseadhoc = ExpenseAdhoc.objects.get(pk=expenseadhoc_id)
#     if request.method == 'GET':
#         form = ExpenseAdhocForm(instance=expenseadhoc)
#     elif request.method == 'POST':
#         form = ExpenseAdhocForm(request.POST, instance=expenseadhoc)     
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("mortgage:expenseadhoc_list", args=()))
#     return render(request, 'mortgage/expenseadhoc_edit.html', {'form': form, 'expenseadhoc': expenseadhoc})


# def expenseadhoc_approve(request, expenseadhoc_id):
#     '''Update approve attribute of existing expenseadhoc object to True.
#     POST: update details of existing object.
#     TODO - if approving an interval expense, update last payment date and 
#     '''
#     expenseadhoc = ExpenseAdhoc.objects.get(pk=expenseadhoc_id)
    
#     # if a loan repayment, must approve in order from oldest to newest
#     # TODO - this block works
#     if expenseadhoc.loan is not None:
#         expenseadhoc_oldest_nonapproved_for_this_loan = ExpenseAdhoc.objects.filter(
#             approved=False, loan=expenseadhoc.loan).order_by('date')[0]
#         if expenseadhoc_oldest_nonapproved_for_this_loan.id != expenseadhoc.id:
#             messages.warning(request, "Must approve oldest loan payment first.")
#             return redirect(reverse('mortgage:for_approval', kwargs={'error': True}))

#     if request.method == 'POST':
    
#         # update approved to True for this expense
#         expenseadhoc.approved = True
            
#         # if payment associated with loan, need to calculate its principal/interest split
#         if expenseadhoc.loan is not None:
#             normalised_interest_rate = 0.01 * expenseadhoc.loan.interest_rate / expenseadhoc.expenseinterval.payments_per_year
            
#             # calculate principal already paid for this loan, by checking for earlier approved payments
#             previous_payments = ExpenseAdhoc.objects.filter(
#                 approved=True,
#                 loan=expenseadhoc.loan,
#                 date__lt=expenseadhoc.date,
#             )
#             if previous_payments:
#                 principal_paid_on_loan_sum = previous_payments.aggregate(Sum("loan_amount_principal"))
#                 principal_paid_on_loan = principal_paid_on_loan_sum['loan_amount_principal__sum']
#             else:
#                 principal_paid_on_loan = 0.

#             # calculate amount remaining to be paid on loan
#             loan_amount_remaining = expenseadhoc.loan.amount - principal_paid_on_loan

#             # calculate principal/interest split based on amount
#             expenseadhoc.loan_amount_interest = loan_amount_remaining * normalised_interest_rate
#             expenseadhoc.loan_amount_principal = expenseadhoc.amount - expenseadhoc.loan_amount_interest

#         # save the changes to the expense (adhoc)
#         expenseadhoc.save()

#         # if this was an expense (interval), need to increment its next payment date
#         if expenseadhoc.expenseinterval is not None:
#             if expenseadhoc.expenseinterval.interval == 'Weekly':
#                 expenseadhoc.expenseinterval.next_payment_date += relativedelta(days=+7)
#             elif expenseadhoc.expenseinterval.interval == 'Fortnightly':
#                 expenseadhoc.expenseinterval.next_payment_date += relativedelta(days=+14)
#             elif expenseadhoc.expenseinterval.interval == 'Monthly':
#                 expenseadhoc.expenseinterval.next_payment_date += relativedelta(months=+1)
#             elif expenseadhoc.expenseinterval.interval == 'Quarterly':
#                 expenseadhoc.expenseinterval.next_payment_date += relativedelta(months=+3)
#             elif expenseadhoc.expenseinterval.interval == 'Annual':
#                 expenseadhoc.expenseinterval.next_payment_date += relativedelta(years=+1)
#             expenseadhoc.expenseinterval.save()

#         return redirect(reverse('mortgage:for_approval', kwargs={'error': False}))


# def for_approval(request, error=False):
#     expensesadhoc = ExpenseAdhoc.objects.filter(approved=False).order_by('expenseinterval', 'date')  
#     return render(request, 'mortgage/for_approval.html', {'expensesadhoc': expensesadhoc, 'error': error})


# def generate_transactions(request):
#     '''
#     POST: generate adhoc transactions from interval transactions.
#     TODO - ensure no duplicate transactions.
#     TODO - only generate oldest transaction for loan repayments.
#     TODO - can probably remove last_payment_date since it can be calculated from associated transactions
#     '''
#     if request.method == 'POST':

#         # iteratively generate expense (adhoc) for each expense (interval)
#         expensesinterval = ExpenseInterval.objects.filter(next_payment_date__lt=timezone.now())
#         for expenseinterval in expensesinterval:

#             # generate list of dates to create individual expenses (adhoc) for
#             approved_payment_dates = expenseinterval.expenseadhoc_set.all().order_by('date')
#             approved_payment_dates = [approved.date for approved in approved_payment_dates]
#             dates_to_generate = []
#             new_date = expenseinterval.next_payment_date
#             while new_date < timezone.now().date():
#                 if new_date not in approved_payment_dates:
#                     dates_to_generate.append(new_date)
#                 if expenseinterval.interval == 'Weekly':
#                     new_date += relativedelta(days=+7)
#                 elif expenseinterval.interval == 'Fortnightly':
#                     new_date += relativedelta(days=+14)
#                 elif expenseinterval.interval == 'Monthly':
#                     new_date += relativedelta(months=+1)
#                 elif expenseinterval.interval == 'Quarterly':
#                     new_date += relativedelta(months=+3)
#                 elif expenseinterval.interval == 'Annual':
#                     new_date += relativedelta(years=+1)
#                 else:
#                     new_date += relativedelta(months=+1)

#             # iteratively generate new expenses (adhoc)
#             for current_date in dates_to_generate:
#                 new_expenseadhoc = ExpenseAdhoc(
#                     description = expenseinterval.description,
#                     amount = expenseinterval.amount,
#                     category = expenseinterval.category,
#                     approved = False,
#                     date = current_date,
#                     user = request.user,
#                     expenseinterval = expenseinterval,
#                     loan = expenseinterval.loan,
#                 )
#                 new_expenseadhoc.save()

#         return redirect(reverse('mortgage:for_approval', kwargs={'error': True}))

#         '''
#         # get all interval expenses where next payment date is in the past
#         expensesinterval = ExpenseInterval.objects.filter(next_payment_date__lt=timezone.now())

#         # iteratively generate expense (adhoc) for each expense (interval)
#         for expenseinterval in expensesinterval:

#             # if a loan, generate only the oldest possible transaction
#             if expenseinterval.loan is not None:

#                 # get queryset containing approved payments for this loan
#                 approved_payments = expenseinterval.loan.expenseadhoc_set.filter(approved=True)
#                 unapproved_payments = expenseinterval.loan.expenseadhoc_set.filter(approved=False)

#                 # if no previously approved payments, generate one transaction
#                 # i.e. a transaction with "next_payment_date"
#                 if not approved_payments:

#                     # do not save it if it has matching date with other unapproved payments
#                     can_be_saved = True
#                     for expenseadhoc in unapproved_payments:
#                         if expenseadhoc.date == expenseinterval.next_payment_date:
#                             can_be_saved = False

#                     # save it
#                     if can_be_saved:
#                         new_expenseadhoc.save()

#                     return redirect(reverse('mortgage:for_approval', kwargs={'error': False}))
                
#                 # TODO - have previous payments, need to work out which ones to do
#                 else:
#                     last_payment_date = approved_payments.latest('date').date
#                     return HttpResponse(last_payment_date)



#             # otherwise
#             else:
#                 return HttpResponse('TODO')
            

#             # 
            
#             dates_to_append = []
#             new_date = expense.next_payment_date

#             while new_date < timezone.now().date():
#                 dates_to_append.append(new_date)

#                 # dates_to_generate = [expense.next_payment_date]

#                 if expense.interval == 'weekly':
#                     new_date += relativedelta(days=+7)
#                 elif expense.interval == 'fortnightly':
#                     new_date += relativedelta(days=+14)
#                 elif expense.interval == 'monthly':
#                     new_date += relativedelta(months=+1)
#                 elif expense.interval == 'quarterly':
#                     new_date += relativedelta(months=+3)
#                 elif expense.interval == 'annual':
#                     new_date += relativedelta(years=+1)

#             if len(dates_to_append) > 0:

#                 for current_date in dates_to_append:

#                     # create a new adhoc expense object
#                     new_expenseadhoc = ExpenseAdhoc(
#                         description = expense.description,
#                         amount = expense.amount,
#                         category = expense.category,
#                         approved = False,
#                         date = current_date,
#                         user = request.user,
#                         expenseinterval = expense,
#                         loan = expense.loan,
#                     )

#                     # save it
#                     new_expenseadhoc.save()

#     return redirect(reverse('mortgage:for_approval', kwargs={'error': True}))
#     '''
    
