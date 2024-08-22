from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.template import loader
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
from django.db import IntegrityError
from django.db.models.constraints import UniqueConstraint
from django.forms.models import model_to_dict
from .models import *
from .forms import *
import json
from datetime import date

# TODO - filter objects by current user, currently retrieves all expenses.
# this will require a group or permissions set up, I expect.
# For now, just hardcode the username.

# TODO - restrict retrieved objects to associated user.
# TODO - restrict access to objects not belonging to user.

# TODO - need to restrict object access based on username/permissions.

# TODO - improve consistency of docstrings.

# TODO - improve consistency of single vs double quotes. Consult PEP for guidance.



@csrf_exempt
def login_user(request):
    """TODO - not authenticating anyone but initial superuser.
    """
    
    # get username and password from request.body JSON
    data = json.loads(request.body)
    username = data['username']
    password = data['password']

    # check if provide credential can be authenticated
    user = authenticate(username=username, password=password)

    # if valid user, login user, otherwise return basic data
    if user is not None:
        login(request, user)
        data = {"username": username, "status": "Authenticated"}
    else:
        data = {"username": username, "status": "Unauthenticated"}
    return JsonResponse(data)

@csrf_exempt
def logout_user(request):
    try:
        logout(request)
        return JsonResponse({"status": "Logged Out"})
    except Exception as err:
        return JsonResponse({"status": err})


@csrf_exempt
def signup_user(request):
    '''Attempt to create a new user based on submission of user form.
    '''
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({"status": "Username already exists"})
        else:
            CustomUser.objects.create_user(username, first_name, last_name, password)
            return JsonResponse({"status": "User created"})


def check_username_exists(request, username):
    if CustomUser.objects.filter(username=username).exists():
        return JsonResponse({"status": "Username already exists"})
    else:
        return JsonResponse({"status": "Username available"})


def blogposts(request):
    json_serializer = serializers.serialize(
        'json',
        BlogPost.objects.all(),
        use_natural_foreign_keys=True,
    )
    return HttpResponse(json_serializer, content_type='application/json')


def expenses(request):
    """
    Retrieves a JSON serialized list of all expenses associated with the currently logged-in user,
    ordered by date in descending order. The serialized data is returned as an HTTP response with
    a content type of 'application/json'.

    Parameters:
    - request (HttpRequest): The HTTP request object containing information about the request.

    Returns:
    - HttpResponse: An HTTP response containing the serialized expense data in JSON format.

    TODO update docstring for consistency with others in code.
    TODO restrict expenses retrieved to those belonging to this user.
    TODO sorts order of objects based on query, now deprecated, will sort directly in frontend instead
    """
    if request.method == 'GET':
        json_serializer = serializers.serialize('json', Expense.objects.all().order_by('-date'), use_natural_foreign_keys=True)
        return HttpResponse(json_serializer, content_type='application/json')

    return JsonResponse({"success": False, "errors": "Method not allowed"})


@csrf_exempt
def expenses_select(request, expense_id):
    """Select specific expense object.

    GET request:
        Return expense object, and expense categories, as JSON.

    TODO - restrict access to only expenses belonging to this user.
    """
    if request.method == 'GET':
        # try to get the object with matching id
        try:
            expense = Expense.objects.get(id=expense_id)
        except Exception as err:
            return JsonResponse({"success": False, "errors": "Expense not found"})

        # TODO somewhat unusual approach to get just one object, try to improve later.
        json_serializer = serializers.serialize('json', [expense], use_natural_foreign_keys=True,)[1:-1]
        json_dict = json.loads(json_serializer)

        # set dictionary of choices for regular payments and loans
        choices_regularpayment = {'None': 'None'}
        for regularpayment in RegularPayment.objects.all():
            choices_regularpayment[regularpayment.description] = regularpayment.description
        choices_loan = {'None': 'None'}
        for loan in Loan.objects.all():
            choices_loan[loan.description] = loan.description
        
        # set additional dictionaries containing choices for select boxes
        json_dict['choices_category'] = dict(Expense.EXPENSE_CHOICES)
        json_dict['choices_regularpayment'] = choices_regularpayment
        json_dict['choices_loan'] = choices_loan

        # return the serialized object
        json_to_return = json.dumps(json_dict)
        return HttpResponse(json_to_return, content_type='application/json')
    
    return JsonResponse({"success": False, "errors": "Invalid request method"})


def expense_form_processing(form_data):
        '''Process raw form data submitted from frontend to create a valid Expense object.
        '''
        # initialise dictionary of processed form data
        form_data_processed = {
            'description': form_data['description'],
            'amount': float(form_data['amount']),
            'category': form_data['category'],
            'date': form_data['date'],  
        }

        # convert html checkbox state to Python Boolean
        if form_data.get('approved') is not None:
            if form_data['approved'] == 'on' or form_data['approved'] == 'true' or form_data['approved'] == 'True':
                form_data_processed['approved'] = True
            else:
                form_data_processed['approved'] = False
        else:
            form_data_processed['approved'] = False

        # get regular payment object if one selected in form
        if form_data['regularpayment'] == 'None':
            form_data_processed['regularpayment'] = None
        else:
            form_data_processed['regularpayment'] = RegularPayment.objects.get(description=form_data['regularpayment'])
        
        # get loan object if one selected in form
        if form_data['loan'] == 'None':
            form_data_processed['loan'] = None
        else:
            form_data_processed['loan'] = Loan.objects.get(description=form_data['loan'])

        # TODO - set user manually for now, automate later
        # user = CustomUser.objects.get(username='colin.c.simpson@gmail.com')
        form_data_processed['user'] = CustomUser.objects.get(username='colin.c.simpson@gmail.com')
        
        return form_data_processed


@csrf_exempt
def expenses_create(request):
    """Create a new expense object, through form submission.

    GET request method:
        Return a Http response containing form fields and expense categories as JSON.

    POST request method:
        Attempt to create a new expense object based on form submitted. 

    TODO - remove hardcoding of username.
    """
    if request.method == 'POST':

        # get raw form data and process to work with backend
        form_data = json.loads(request.body)
        form_data_processed = expense_form_processing(form_data)

        # try except block to get form object and set foreign keys
        try:
            form = ExpenseForm(form_data_processed)
            form.user = form_data_processed['user']
            form.regularpayment = form_data_processed['regularpayment']
            form.loan = form_data_processed['loan']
        except Exception as err:
            return JsonResponse({"success": False, 'errors': 'unknown error in submitting form'})
        
        # create new expense if form is valid, otherwise return error
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({"success": True})
            except Exception as err:
                print('something went wrong with save', err)
                return JsonResponse({"success": False, 'errors': str(err)})
        else:
            print('form not valid', form.errors)
            return JsonResponse({"success": False, 'errors': form.errors})
    
    elif request.method == 'GET':

        # set dictionary of choices for regular payments and loans
        choices_regularpayment = {'None': 'None'}
        for regularpayment in RegularPayment.objects.all():
            choices_regularpayment[regularpayment.description] = regularpayment.description
        choices_loan = {'None': 'None'}
        for loan in Loan.objects.all():
            choices_loan[loan.description] = loan.description
        
        # create JSON response
        json_serializer = json.dumps({
            'pk': None,
            'fields': {
                'description': None,
                'amount': None,
                'category': 'Food',
                'date': str(date.today()),
                'approved': 'on',
                'regularpayment': 'None',
                'loan': 'None',
            },
            'choices_category': dict(Expense.EXPENSE_CHOICES),
            'choices_regularpayment': choices_regularpayment,
            'choices_loan': choices_loan,
        })
        return HttpResponse(json_serializer, content_type='application/json')
    
    return JsonResponse({"success": False, "errors": "Invalid request method"})


@csrf_exempt
def expenses_edit(request, expense_id):
    """Update object fields based on form submission.
    
    TODO restrict access to only user who owns object.
    """
    if request.method == 'POST':

        # get expense object
        try:
            expense = Expense.objects.get(id=expense_id)
        except Exception as err:
            return JsonResponse({"success": False, 'errors': err})

        # get raw data from form and make call to function for processing
        form_data = json.loads(request.body)
        form_data_processed = expense_form_processing(form_data)
        print(form_data)
        print(form_data_processed)

        # update object with processed form data
        form = ExpenseForm(form_data_processed, instance=expense)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, 'errors': form.errors, 'status': 400})
    return JsonResponse({"success": False, "errors": "Invalid request method"})


@csrf_exempt
def expenses_delete(request, expense_id):
    if request.method == 'POST':
        expense = Expense.objects.get(id=expense_id)
        expense.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "errors": "Invalid request method"})


def regularpayments(request):
    """Return a HTTP response containing all regular payments as JSON.

    """
    if request.method == 'GET':
        json_serializer = serializers.serialize(
            'json',
            RegularPayment.objects.all(),
            use_natural_foreign_keys=True,
        )
        return HttpResponse(json_serializer, content_type='application/json')
    return JsonResponse({"success": False, "errors": "Method not allowed"})


@csrf_exempt
def regularpayments_create(request):
    """Create a new regular payment object through form submission.

    GET request:
        Return Http response containing expense categories and intervals as JSON.

    POST request:
        Attempt to create the new regular payment object.

    TODO - remove hardcoded user.
    TODO - check/improve error handling for invalid form submission.
    """
    # attempt to post data collected by frontend form to create new object
    if request.method == 'POST':
        
        # preprocess the form data
        form_data = json.loads(request.body)
        form_data['amount'] = float(form_data['amount'])

        # get loan object if one selected in form
        if form_data['loan'] == 'None':
            loan = None
        else:
            loan = Loan.objects.get(description=form_data['loan'])

        print(form_data, loan)

        # try except block to get form object
        try:
            form = RegularPaymentForm(form_data)
        except Exception as err:
            return JsonResponse({"success": False, 'errors': 'unknown error in submitting form'})
        


        # create new object if form is valid, otherwise return error
        if form.is_valid():
            print('new object created successfully')
            try:
                regularpayment = form.save(commit=False)
                regularpayment.user = CustomUser.objects.get(username='colin.c.simpson@gmail.com')
                # if loan is not None:
                #     regularpayment.loan = loan
                regularpayment.save()
                return JsonResponse({"success": True})
            except Exception as err:
                return JsonResponse({"success": False, 'errors': str(err)})
        else:
            print('failed for reason\n', form.errors)
            return JsonResponse({"success": False, 'errors': form.errors})
    
    # fetch data needed for form in a GET request
    elif request.method == 'GET':
        choices_loan = {'None': 'None'}
        for loan in Loan.objects.all():
            choices_loan[loan.description] = loan.description
        json_serializer = json.dumps({
            'pk': None,
            'fields': {
                'description': None,
                'amount': None,
                'category': None,
                'interval': None,
                'firstpaymentdate': None,
                'nextpaymentdate': None,
                'loan': None,
            },
            'choices_category': dict(RegularPayment.EXPENSE_CHOICES),
            'choices_interval': dict(RegularPayment.INTERVAL_CHOICES),
            'choices_loan': choices_loan,
        })
        return HttpResponse(json_serializer, content_type='application/json')
    return JsonResponse({"success": False, "errors": "Invalid request method"})


@csrf_exempt
def regularpayments_select(request, regularpayment_id):
    """Obtain information on a specific regular payment.

    GET request:
        Return Http response containing regular payment information, as well as
        iterables containing expense categories and intervals.

    TODO - restrict obtaining regularpayment to those belonging only to user.
    TODO - check/improve error handling.
    """
    if request.method == 'GET':

        # try to get regular payment object
        try: 
            regularpayment = RegularPayment.objects.get(id=regularpayment_id)
        except Exception as err:
            return JsonResponse({"success": False, "errors": "Regular payment not found"})
        
        # create dict of choices for loan
        choices_loan = {'None': 'None'}
        for loan in Loan.objects.all():
            choices_loan[loan.description] = loan.description

        # serialize object and return
        json_serializer = serializers.serialize('json', [regularpayment], use_natural_foreign_keys=True)[1:-1]
        json_dict = json.loads(json_serializer)
        json_dict['choices_category'] = dict(RegularPayment.EXPENSE_CHOICES)
        json_dict['choices_interval'] = dict(RegularPayment.INTERVAL_CHOICES)
        json_dict['choices_loan'] = choices_loan
        json_to_return = json.dumps(json_dict)
        return HttpResponse(json_to_return, content_type='application/json')
    
    return JsonResponse({"success": False, "errors": "Invalid request method"})


@csrf_exempt
def regularpayments_edit(request, regularpayment_id):
    """Update object fields based on form submission. 

    TODO - currently hardcoded to specific user, need to fix.
    """
    if request.method == 'POST':

        # try to get regular payment object
        try:
            regularpayment = RegularPayment.objects.get(id=regularpayment_id)
        except Exception as err:
            return JsonResponse({"success": False, 'errors': err})

        # get form using posted data
        form_data = json.loads(request.body)

        # set user in form data
        # form_data['user'] = CustomUser.objects.get(username='colin.c.simpson@gmail.com')

        form = RegularPaymentForm(form_data, instance=regularpayment)

        print(form_data)
        # TODO - currently frontend not sending loan data, probably aLSO Need to manually set user
        # form.user = CustomUser.objects.get(username='colin.c.simpson@gmail.com')

        # if form is valid, update object, otherwise return error
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            print('not valid, errors', form.errors)
            return JsonResponse({"success": False, 'errors': form.errors, 'status': 400})
    
    return JsonResponse({"success": False, "errors": "Invalid request method"})

        