from django.urls import path
from . import views
from .views import *

app_name = "backend"
urlpatterns = [
    # path('users/', views.users, name='users'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('blogposts/', views.blogposts, name='blogposts'),
    path('expenses/', views.expenses, name='expenses'),
]