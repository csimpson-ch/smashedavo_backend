from django.urls import path
from . import views
from .views import *

app_name = "backend"
urlpatterns = [
    # path('users/', views.users, name='users'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('check_username_exists/<username>', views.check_username_exists, name='check_username_exists'),
    path('blogposts/', views.blogposts, name='blogposts'),
    path('expenses/', views.expenses, name='expenses'),
    path('regularpayments/', views.regularpayments, name='regularpayments'),
]