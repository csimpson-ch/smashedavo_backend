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
    path('expenses/create/', views.expenses_create, name='expenses_create'),
    path('expenses/<int:expense_id>/', views.expenses_select, name='expenses_select'),
    path('expenses/<int:expense_id>/edit/', views.expenses_edit, name='expenses_edit'),
    path('expenses/<int:expense_id>/delete/', views.expenses_delete, name='expenses_delete'),
    path('regularpayments/', views.regularpayments, name='regularpayments'),
    path('regularpayments/create/', views.regularpayments_create, name='regularpayments_create'),
    path('regularpayments/<int:regularpayment_id>/', views.regularpayments_select, name='regularpayments_select'),
    path('regularpayments/<int:regularpayment_id>/edit/', views.regularpayments_edit, name='regularpayments_edit'),
    # path('expense_category_choices/', views.expense_category_choices, name='expense_category_choices'),
]