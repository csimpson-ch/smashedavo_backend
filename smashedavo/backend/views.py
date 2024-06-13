from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound, JsonResponse
from django.core import serializers
# from rest_framework import serializers as rest_framework_serializers
from django.template import loader
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

from .models import *


# class BlogPostSerializer(rest_framework_serializers.ModelSerializer):
#     '''Use the rest framework serializer to create custom class
#     '''
#     user = rest_framework_serializers.CharField(source ='user.username')
#     pub_date = rest_framework_serializers.DateTimeField(format="%Y-%m-%d")

#     class Meta:
#         model = BlogPost
#         fields = '__all__'
#         # fields = ['id', 'title', 'text', 'pub_date', 'user']


def blogposts(request):

    json_serializer = serializers.serialize(
        'json',
        BlogPost.objects.all(),
        use_natural_foreign_keys=True,
        use_natural_primary_keys=True,
    )

    # blogposts_as_json = django_serializers.serialize('json', BlogPost.objects.all(), cls=BlogPostSerializer)
    return HttpResponse(json_serializer, content_type='application/json')


def users(request):
    json_serializer = serializers.serialize(
        'json',
        CustomUser.objects.all(),
        use_natural_foreign_keys=True,
        use_natural_primary_keys=True
    )
    return HttpResponse(json_serializer, content_type='application/json')