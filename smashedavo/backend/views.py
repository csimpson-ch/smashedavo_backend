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
from .models import *
from .forms import *
import json

# TODO - filter objects by current user, currently retrieves all expenses.
# this will require a group or permissions set up, I expect.
# For now, just hardcode the username.

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
    # TODO - deprecated. Formerly used to determine which column to order by.
    # request_orderby = request.GET.get('orderby')
    # if request_orderby == 'amount':
    #     orderby = 'amount'
    # elif request_orderby == 'description':
    #     orderby = 'description'
    # elif request_orderby == 'category':
    #     orderby = 'category'
    # else:
    #     orderby = 'date'
    # if request.GET.get('ordering') == 'desc':
    #     orderby = '-'+orderby

    json_serializer = serializers.serialize(
        'json',
        Expense.objects.all().order_by('-date'),
        use_natural_foreign_keys=True,
    )
    return HttpResponse(json_serializer, content_type='application/json')


@csrf_exempt
def expenses_select(request, expense_id):
    """Select specific expense object.

    GET request:
        Return expense object, and expense categories, as JSON.

    TODO - restrict access to only expenses belonging to this user.
    """
    if request.method == 'GET':
        expense = Expense.objects.get(id=expense_id)
        # TODO somewhat unusual approach to get just one object, try to improve later.
        json_serializer = serializers.serialize('json', [expense])[1:-1]
        json_dict = json.loads(json_serializer)
        json_dict['category_choices'] = dict(Expense.EXPENSE_CHOICES)
        json_to_return = json.dumps(json_dict)
        return HttpResponse(json_to_return, content_type='application/json')
    return JsonResponse({"success": False, "errors": "Invalid request method"})


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
        data = json.loads(request.body)
        try:
            form = ExpenseForm(data)
        except:
            return JsonResponse({"success": False, 'errors': 'unknown error in submitting form'})
        if form.is_valid():
            try:
                expense = form.save(commit=False)
                expense.user = CustomUser.objects.get(username='colin.c.simpson@gmail.com')
                expense.save()
                return JsonResponse({"success": True})
            except Exception as err:
                return JsonResponse({"success": False, 'errors': str(err)})
        else:
            return JsonResponse({"success": False, 'errors': form.errors})
    elif request.method == 'GET':
        dict_to_dump = {
            'pk': None,
            'fields': {
                'description': None,
                'amount': None,
                'category': None,
                'date': None,
                'approved': False, 
            },
            'category_choices': dict(Expense.EXPENSE_CHOICES),
        }
        json_serializer = json.dumps(dict_to_dump)
        return HttpResponse(json_serializer, content_type='application/json')
    return JsonResponse({"success": False, "errors": "Invalid request method"})


@csrf_exempt
def expenses_edit(request, expense_id):
    """Update object fields based on form submission.
    
    TODO restrict access to only user who owns object.
    """
    if request.method == 'POST':
        try:
            expense = Expense.objects.get(id=expense_id)
        except Exception as err:
            return JsonResponse({"success": False, 'errors': err})
        form_data = json.loads(request.body)
        form = ExpenseForm(form_data, instance=expense)
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

    TODO - restrict to regular payments belonging only to the user.
    """
    json_serializer = serializers.serialize(
        'json',
        RegularPayment.objects.all(),
        use_natural_foreign_keys=True,
    )
    return HttpResponse(json_serializer, content_type='application/json')


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
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            form = RegularPaymentForm(data)
        except Exception as err:
            return JsonResponse({"success": False, 'errors': 'unknown error in submitting form'})
        if form.is_valid():
            try:
                regularpayment = form.save(commit=False)
                regularpayment.user = CustomUser.objects.get(username='colin.c.simpson@gmail.com')
                regularpayment.save()
                return JsonResponse({"success": True})
            except Exception as err:
                return JsonResponse({"success": False, 'errors': str(err)})
        else:
            return JsonResponse({"success": False, 'errors': form.errors})
    elif request.method == 'GET':
        json_serializer = json.dumps({
            'category_choices': dict(RegularPayment.EXPENSE_CHOICES),
            'interval_choices': dict(RegularPayment.INTERVAL_CHOICES)
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
        try: 
            regularpayment = RegularPayment.objects.get(id=regularpayment_id)
        except Exception as err:
            return JsonResponse({"success": False, "errors": "Regular payment not found"})
        json_serializer = serializers.serialize('json', [regularpayment])[1:-1]
        json_dict = json.loads(json_serializer)
        json_dict['category_choices'] = dict(RegularPayment.EXPENSE_CHOICES)
        json_dict['interval_choices'] = dict(RegularPayment.INTERVAL_CHOICES)
        json_to_return = json.dumps(json_dict)
        return HttpResponse(json_to_return, content_type='application/json')
    return JsonResponse({"success": False, "errors": "Invalid request method"})


@csrf_exempt
def regularpayments_edit(request, regularpayment_id):
    """
    TODO - currently hardcoded to specific user, need to fix.
    """
    if request.method == 'POST':
        regularpayment = RegularPayment.objects.get(id=regularpayment_id)
        form_data = json.loads(request.body)
        print('post request for id:', regularpayment_id, '\n', form_data)
        form = RegularPaymentForm(form_data, instance=regularpayment)
        if form.is_valid():
            form.save()
            print('success')
            return JsonResponse({"success": True})
        else:
            print('fail')
            return JsonResponse({"success": False, 'errors': form.errors, 'status': 400})
    return JsonResponse({"success": False, "errors": "Invalid request method"})



