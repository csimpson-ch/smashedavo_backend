from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.template import loader
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
from .models import *
import json

@requires_csrf_token
def login_user(request):
    
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
        return JsonResponse({"status": "Logged out"})
    except:
        return JsonResponse({"status": "Error"})


def blogposts(request):
    json_serializer = serializers.serialize(
        'json',
        BlogPost.objects.all(),
        use_natural_foreign_keys=True,
    )
    return HttpResponse(json_serializer, content_type='application/json')


def expenses(request):
    json_serializer = serializers.serialize(
        'json',
        Expense.objects.filter(user__username=request.user).order_by("-date")[:],
        # Expense.objects.all(),
        use_natural_foreign_keys=True,
    )
    return HttpResponse(json_serializer, content_type='application/json')


