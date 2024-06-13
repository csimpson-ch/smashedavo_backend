from django.urls import path
from . import views
from .views import *

app_name = "backend"
urlpatterns = [
    path('users/', views.users, name='users'),
    path('blogposts/', views.blogposts, name='blogposts'),
]