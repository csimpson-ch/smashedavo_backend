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
from .forms import ExpenseForm
import json

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
    except:
        return JsonResponse({"status": "Error"})


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
    TODO - filter by user, currently retrieves all expenses.

    Retrieves a JSON serialized list of all expenses associated with the currently logged-in user,
    ordered by date in descending order. The serialized data is returned as an HTTP response with
    a content type of 'application/json'.

    Parameters:
    - request (HttpRequest): The HTTP request object containing information about the request.

    Returns:
    - HttpResponse: An HTTP response containing the serialized expense data in JSON format.
    """
    # determine which column to order by
    request_orderby = request.GET.get('orderby')
    if request_orderby == 'amount':
        orderby = 'amount'
    elif request_orderby == 'description':
        orderby = 'description'
    elif request_orderby == 'category':
        orderby = 'category'
    else:
        orderby = 'date'

    # change to desc order if requested, otherwise asc by default
    if request.GET.get('ordering') == 'desc':
        orderby = '-'+orderby

    json_serializer = serializers.serialize(
        'json',
        Expense.objects.all().order_by(orderby),
        use_natural_foreign_keys=True,
    )
    return HttpResponse(json_serializer, content_type='application/json')


def regularpayments(request):
    json_serializer = serializers.serialize(
        'json',
        RegularPayment.objects.all(),
        use_natural_foreign_keys=True,
    )
    return HttpResponse(json_serializer, content_type='application/json')


@csrf_exempt
def expense_create(request):
    '''TODO - update so user is set automatically, instead of in post request.
    '''
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        try:
            form = ExpenseForm(data)
        except:
            return JsonResponse({"success": False, 'errors': 'unknown error in submitting form'})
        if form.is_valid():
            try:
                bbb = form.save(commit=False)
                bbb.user = CustomUser.objects.get(username='colin.c.simpson@gmail.com')
                # bbb.regular_payment = RegularPayment.objects.get(description=data['regularpayment'])
                # bbb.save()
                return JsonResponse({"success": True})
            except Exception as err:
                return JsonResponse({"success": False, 'errors': str(err)})

        else:
            return JsonResponse({"success": False, 'errors': form.errors})
    return JsonResponse({"success": False, "errors": "Invalid request method"})


@csrf_exempt
def expense_update(request, expense_id):
    '''TODO - currently hardcoded to specific user, need to fix.
    '''
    expense = Expense.objects.get(id=expense_id)
    if request.method == 'POST':
        form_data = json.loads(request.body)
        form = ExpenseForm(form_data, instance=expense)
        # print(form)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, 'errors': form.errors})
    elif request.method == 'GET':
        json_serializer = serializers.serialize('json', [expense])[1:-1]
        return HttpResponse(json_serializer, content_type='application/json')
    return JsonResponse({"success": False, "errors": "Invalid request method"})


@csrf_exempt
def expense_category_choices(request):
    json_serializer = json.dumps(dict(Expense.EXPENSE_CHOICES))
    return HttpResponse(json_serializer, content_type='application/json')
