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
    json_serializer = serializers.serialize(
        'json',
        # Expense.objects.filter(user__username=request.user).order_by("-date")[:],
        Expense.objects.all(),
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
